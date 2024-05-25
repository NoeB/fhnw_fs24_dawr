### File Helper to extract data from the HTML FILE
### Extracted from: preproccesing_notebook.ipynb

from typing import Dict, List
import pandas as pd
import numpy as np
import scrapy
from scrapy.selector import Selector
from datetime import datetime, timedelta
import locale
import re
from dataclasses import dataclass

locale.setlocale(locale.LC_TIME, 'de_DE')

# {'Klettern Schwierigkeit:', 'Geo-Tags:', 'Abstieg:', 'Wegpunkte:', 'Zufahrt zum Ankunftspunkt:', 'Wandern Schwierigkeit:', 'Ski Schwierigkeit:', 'Strecke:', 'Zufahrt zum Ausgangspunkt:', 'Mountainbike Schwierigkeit:', 'Aufstieg:', 'Region:', 'Hochtouren Schwierigkeit:', 'Zeitbedarf:', 'Unterkunftmöglichkeiten:', 'Schneeshuhtouren Schwierigkeit:', 'Tour Datum:', 'Kartennummer:', 'Klettersteig Schwierigkeit:'}
columns =  ['Klettern Schwierigkeit:', 'Geo-Tags:', 'Abstieg:', 'Wegpunkte:', 'Zufahrt zum Ankunftspunkt:', 'Wandern Schwierigkeit:', 'Ski Schwierigkeit:', 'Strecke:', 'Zufahrt zum Ausgangspunkt:', 'Mountainbike Schwierigkeit:', 'Aufstieg:', 'Region:', 'Hochtouren Schwierigkeit:', 'Zeitbedarf:', 'Unterkunftmöglichkeiten:', 'Schneeshuhtouren Schwierigkeit:', 'Tour Datum:', 'Kartennummer:', 'Klettersteig Schwierigkeit:']

def parse_region(region_raw: str)-> Dict[str, str]:
    """
    Extracts the region from the raw HTML.
    
    Parameters:
    region_raw (str): The raw HTML containing the region.

    Returns:
    Dict[str, str]: A dictionary containing the region information.
    """
    if region_raw is None:
        return None
    document = Selector(text=region_raw)
    a_tags = document.css('a')
    output = {}
    for i, a_tag in enumerate(a_tags):
        content = a_tag.css('::text').get()
        if i == 1:
            output["country"] = content.strip()
        else:
            output[f"region_{i}_content"] = content.strip()
    return output



def parse_tour_date(tour_date_raw: str) -> datetime.date:
    """
    Extracts the tour date from the raw HTML.
    
    Parameters:
    tour_date_raw (str): The raw HTML containing the tour date.

    Returns:
    datetime.date: The tour date.
    """
    locale.setlocale(locale.LC_TIME, 'de_DE')# Just to be sure
    if tour_date_raw is None:
        return None
    return datetime.strptime(tour_date_raw, '%d %B %Y').date()


icon_lookup = {
    "https://s.hikr.org/r4icons/ico2_point_s.png": "other",
    "https://s.hikr.org/r4icons/ico2_ruin_s.png": "ruin",
    "https://s.hikr.org/r4icons/ico2_cave_s.png": "cave",
    "https://s.hikr.org/r4icons/ico2_ort_s.png": "location",
    "https://s.hikr.org/r4icons/ico2_bridg_s.png": "bridge",
    "https://s.hikr.org/r4icons/ico2_pass_s.png": "pass",
    "https://s.hikr.org/r4icons/ico2_viafe_s.png": "via_ferrata", #Klettersteig
    "https://s.hikr.org/r4icons/ico2_climb_s.png": "climb",
    "https://s.hikr.org/r4icons/ico2_wand_s.png": "wall",
    "https://s.hikr.org/r4icons/ico2_lake_s.png": "lake",
    "https://s.hikr.org/r4icons/ico2_peak_s.png": "peak",
    "https://s.hikr.org/r4icons/ico2_hut_s.png": "hut",
    "https://s.hikr.org/r4icons/ico2_eisfa_s.png": "icefall",
}


@dataclass
class Waypoint:
    image: str
    name_raw: str
    type: str
    waypoint_url: str
    height: int
    name: str
    peak_id: str


def parse_waypoints(wegpunkte_raw: str) -> List[Waypoint]:
    """
    Extracts the waypoints from the raw HTML.
    
    Parameters:
    wegpunkte_raw (str): The raw HTML containing the waypoints.
    
    Returns:
    List[Waypoint]: A list of waypoints.
    """
    if wegpunkte_raw is None:
        return None
    document = Selector(text=wegpunkte_raw)
    list_items = document.css('li:not([class])')  # This is a special case for some of the waypoints also have subpoints which I ignore for now: example: post24156.html
   
    
    output = []
    for i, li in enumerate(list_items):
        image = li.css('img::attr(src)').get()
        name_raw = li.css('a::text').get().strip()
        waypoint_url = li.css('a::attr(href)').get()
        peak_id = li.css('a::attr(href)').re_first(r'(\d+)')
        
        regex_pattern = r"(.*?)\s+(\d+)\s+m" # https://regex101.com/r/MNWWxW/1


        if image is None:
            print(f"Image not found for {name_raw}")
        match = re.search(regex_pattern, name_raw)
        height = None
        name = None
        if match:
            name = match.group(1).strip()
            height = int(match.group(2))
        waypoint = Waypoint(
            image=image,
            name_raw=name_raw,
            type=icon_lookup.get(image, None),
            waypoint_url=waypoint_url,
            height=height,
            name=name,
            peak_id=peak_id
        )
        output.append(waypoint)
    return output




@dataclass
class HikingDifficulty:
    hiking_difficulty: str
    hiking_difficulty_description: str

def parse_hiking_difficulty(hiking_difficulty_raw: str) -> HikingDifficulty:
    """
    Extracts the hiking difficulty from the raw HTML.
    
    Parameters:
    hiking_difficulty_raw (str): The raw HTML containing the hiking difficulty.
    
    Returns:
    HikingDifficulty: The hiking difficulty.
    """
    if hiking_difficulty_raw is None:
        return None
    document = Selector(text=hiking_difficulty_raw)
    regex_pattern = r"(T\d[+-]?)\s*-\s*(.*)" #https://regex101.com/r/otbIAQ/1
    a_tags = document.css('a')
    assert len(a_tags) == 1, "Several A tags"
    match = re.search(regex_pattern, a_tags[0].css('::text').get().strip())
    if match:
        return HikingDifficulty(
            hiking_difficulty=match.group(1),
            hiking_difficulty_description=match.group(2)
        )
    return  None



def parse_duration(duration_raw: str) -> timedelta:
    """
    Extracts the duration from the raw HTML.
    
    Parameters:
    duration_raw (str): The raw HTML containing the duration.
    
    Returns:
    timedelta: The duration.
    """
    if duration_raw is None:
        return None
    regex_pattern = re.compile(r"(\d+)?\s?(?:Tage|days)?\s?(\d{1,2}(?::\d{2}))?")  #https://regex101.com/r/rVlCVe/1
    match = re.search(regex_pattern, duration_raw)
    if match:
        days = int(match.group(1)) if match.group(1) else 0
        hours_minutes = match.group(2) if match.group(2) else "0:00"
        hours, minutes = map(int, hours_minutes.split(":"))
        
        return timedelta(days=days, hours=hours, minutes=minutes)
        
    return None



def parse_descent(descent_raw: str) -> int:
    """
    Extracts the descent from the raw HTML.
    
    Parameters:
    descent_raw (str): The raw HTML containing the descent.
    """
    if descent_raw is None:
        return None
    return int(descent_raw.split(' ')[0].strip())


@dataclass
class ClimbingDifficulty:
    climbing_difficulty: str
    climbing_difficulty_description: str

def parse_climbing_difficulty(climbing_difficulty_raw: str) -> ClimbingDifficulty:
    if climbing_difficulty_raw is None:
        return None
    document = Selector(text=climbing_difficulty_raw)
    regex_pattern = r"(K\d[+-]?)\s*-\s*(.*)" #https://regex101.com/r/otbIAQ/1
    a_tags = document.css('a')
    assert len(a_tags) == 1, "Several A tags"
    match = re.search(regex_pattern, a_tags[0].css('::text').get().strip())
    if match:
        return ClimbingDifficulty(
            climbing_difficulty=match.group(1),
            climbing_difficulty_description=match.group(2)
        )
    return None


def parse_high_tour_difficulty(high_tour_difficulty_raw: str) -> str:
    """
    Extracts the high tour difficulty from the raw HTML.
    
    Parameters:
    high_tour_difficulty_raw (str): The raw HTML containing the high tour difficulty.
    
    Returns:
    str: The high tour difficulty.
    """
    if high_tour_difficulty_raw is None:
        return None
    document = Selector(text=high_tour_difficulty_raw)
    a_tags = document.css('a')
    assert len(a_tags) == 1, "Several A tags"
    return a_tags[0].css('::text').get().strip()



@dataclass
class MountainBikeDifficulty:
    mountainbike_difficulty: str
    mountainbike_difficulty_description: str

def parse_mountainbike_difficulty(mountainbike_difficulty_raw: str) -> MountainBikeDifficulty:
    if mountainbike_difficulty_raw is None:
        return None
    document = Selector(text=mountainbike_difficulty_raw)
    regex_pattern = r"(S\d[+-]?)\s*-\s*(.*)" #https://regex101.com/r/otbIAQ/1
    a_tags = document.css('a')
    assert len(a_tags) == 1, "Several A tags"
    match = re.search(regex_pattern, a_tags[0].css('::text').get().strip())
    if match:
        return MountainBikeDifficulty(
            mountainbike_difficulty=match.group(1),
            mountainbike_difficulty_description=match.group(2)
        )
    return None


def parse_via_ferrata_difficulty(via_ferrata_difficulty_raw: str) -> str:
    """
    Extracts the via ferrata difficulty from the raw HTML.
    
    Parameters:
    via_ferrata_difficulty_raw (str): The raw HTML containing the via ferrata difficulty.
    
    Returns:
    str: The via ferrata difficulty.
    """
    if via_ferrata_difficulty_raw is None:
        return None
    document = Selector(text=via_ferrata_difficulty_raw)
    a_tags = document.css('a')
    assert len(a_tags) == 1, "Several A tags"
    return a_tags[0].css('::text').get().strip()



def parse_ski_difficulty(ski_difficulty_raw: str) -> str:
    """
    Extracts the ski difficulty from the raw HTML.
    
    Parameters:
    ski_difficulty_raw (str): The raw HTML containing the ski difficulty.
    
    Returns:
    str: The ski difficulty.
    """
    if ski_difficulty_raw is None:
        return None
    document = Selector(text=ski_difficulty_raw)
    a_tags = document.css('a')
    assert len(a_tags) == 1, "Several A tags"
    return a_tags[0].css('::text').get().strip()




@dataclass
class SnowshoeTourDifficulty:
    snowshoe_tour_difficulty: str
    snowshoe_tour_difficulty_description: str

def parse_snowshoe_tour_difficulty(snowshoe_tour_difficulty_raw: str) -> SnowshoeTourDifficulty:
    """
    Extracts the snowshoe tour difficulty from the raw HTML.
    
    Parameters:
    snowshoe_tour_difficulty_raw (str): The raw HTML containing the snowshoe tour difficulty.
    
    Returns:
    SnowshoeTourDifficulty: The snowshoe tour difficulty.
    """
    if snowshoe_tour_difficulty_raw is None:
        return None
    document = Selector(text=snowshoe_tour_difficulty_raw)
    regex_pattern = r"(WT\d[+-]?)\s*-\s*(.*)" #https://regex101.com/r/otbIAQ/1
    a_tags = document.css('a')
    assert len(a_tags) == 1, "Several A tags"
    match = re.search(regex_pattern, a_tags[0].css('::text').get().strip())
    if match:
        return SnowshoeTourDifficulty(
            snowshoe_tour_difficulty=match.group(1),
            snowshoe_tour_difficulty_description=match.group(2)
        )
    return None


def parse_ascent(ascent_raw: str) -> int:
    """
    Extracts the ascent from the raw HTML.
    
    Parameters:
    ascent_raw (str): The raw HTML containing the ascent.
    
    Returns:
    int: The ascent.
    """
    if ascent_raw is None:
        return None
    return int(ascent_raw.split(' ')[0].strip())

def count_photos(html_content: str) -> int:
    """
    Count the number of photos in the HTML content.
    
    Parameters:
    html_content (str): The raw HTML content.
    
    Returns:
    int: The number of photos.
    """
    photo_ids = re.findall(r'photo_id:(\d+)', html_content)
    return len(photo_ids)



@dataclass
class Peak:
    latitude: float
    longitude: float
    name: str
    height: int
    id: int

def parse_peak_map(html_content: str) -> list[Peak]:
    """
    Parse the peak map from the HTML content.
    
    Parameters:
    html_content (str): The raw HTML content.
    
    Returns:
    list[Peak]: A list of peaks.
    """
    pattern = r'pizs\.push\(\{.*?piz_lat:([\d.]+),.*?piz_lon:([\d.]+),.*?piz_name:"(.*?)",.*?piz_height:(\d+),.*?piz_id:(\d+).*?\}\)' ## Regex: https://regex101.com/r/3EiAxt/1
    matches = re.findall(pattern, html_content, re.DOTALL)
        
    # Parse the peak information and yield the data
    peaks = []
    for match in matches:
        peak = Peak(
            latitude=float(match[0]),
            longitude=float(match[1]),
            name=match[2],
            height=int(match[3]),
            id=int(match[4])
        )
        peaks.append(peak)
    return peaks


@dataclass
class TourPartner:
    name: str
    user_id: str

def parse_tour_partners(html_content: str) -> List[TourPartner]:
    """
    Parse the tour partners from the HTML content.  
    
    Parameters:
    html_content (str): The raw HTML content.
    
    Returns:
    List[TourPartner]: A list of tour partners.
    """
    document = Selector(text=html_content)
    ## Only use the div whhich contains: <b>Tourengänger:</b>
    div = document.xpath('//div[contains(@class, "div15") and contains(.//b/text(), "Tourengänger:")]')


    partners = []
    for a in div.css('a'):
        url = a.css('::attr(href)').get()
        partners.append({
            'name': a.css('::text').get(),
            'user_id': url.split('/')[-2]
        })

    return partners


def parse_page_views(html_content: str) -> int:
    """
    Parse the page views from the HTML content.
    
    Parameters:
    html_content (str): The raw HTML content.

    Returns:
    int: The number of page views.
    """
    document = Selector(text=html_content)
    div = document.css('div[style="text-align:center;color:#666;font-size:0.814em"]')
    views = int(div.css('b::text').get())
    return views