import os
import pandas as pd
from io import BytesIO
from typing import TypedDict, Dict, Optional, List, Set
import lib.query as query
import lib.openstreetmap as openstreetmap
import lib.geoadmin as geoadmin

data_path = './data'

# Ensure the directory exists
os.makedirs(data_path, exist_ok=True)
os.makedirs(data_path + '/raw', exist_ok=True)
os.makedirs(data_path + '/raw/bund', exist_ok=True)

# read the commune files: assignment2/data/raw/bund/gemeinde.csv

# read the file
commune_df = pd.read_csv(data_path + '/raw/bund/gemeinde.csv')



# SHould be type arras of dict
geofeatures: List[Dict[str, str]] = []

country_cords = openstreetmap.get_border_coords("CH")

for index, row in commune_df.iterrows():
    bfs_id = row['BFS-Gde Nummer']
    # fetch the data from the Overpass API
    response_crosswalks = openstreetmap.fetch_overpass_api(query.get_crosswalk_count(bfs_id))
    response_traffic_signals = openstreetmap.fetch_overpass_api(query.get_traffic_signals_count(bfs_id))
    house_count = openstreetmap.fetch_overpass_api(query.get_house_count(bfs_id))
    appartment_count = openstreetmap.fetch_overpass_api(query.get_appartment_count(bfs_id))
    accidents_count = geoadmin.get_accidents_count(bfs_id)
     # avg_distance_to_townhall = openstreetmap.get_building_distances(bfs_id)
    distance_to_border = openstreetmap.get_distance_to_border(bfs_id, country_cords)
   # commune_area, commune_area_in_water = openstreetmap.get_commune_area(bfs_id)
    geofeatures.append({
        'bfs_id': bfs_id,
        'crosswalks_nr': response_crosswalks["elements"][0]["tags"]["total"],
        'traffic_signals_nr': response_traffic_signals["elements"][0]["tags"]["total"],
        'house_count': house_count["elements"][0]["tags"]["total"],
        'appartment_count': appartment_count["elements"][0]["tags"]["total"],
        'accidents_count': accidents_count,
       # 'avg_distance_to_townhall': avg_distance_to_townhall,
        'distance_to_border': distance_to_border,
        #'commune_area': commune_area,
       # 'commune_area_in_water': commune_area_in_water
       ## Add all from gemeinde except: Gemeindecode
    })


# convert to a DataFrame

geofeatures_df = pd.DataFrame(geofeatures)
# save the DataFrame to a CSV file
geofeatures_df.to_csv(data_path + '/geofeatures.csv', index=False)


