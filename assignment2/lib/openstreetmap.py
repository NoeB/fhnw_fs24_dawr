import requests
import math



def fetch_overpass_api(query: str) -> dict:
    """
    Fetch data from the Overpass API
    :param query: Overpass QL query
    :return: JSON response
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, params={'data': query})
    if response.status_code != 200:
        print(f"Error fetching data from Overpass API: {response.status_code}")
    return response.json()



def get_building_distances(bfs_id: int) -> float:
    """
    Get the average distance from buildings to the city center in a given area
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query to retrieve building coordinates within the city
    building_query = f"""
    [out:json];
    area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_id}]->.searchArea;
    (
      node(area.searchArea)[building];
      way(area.searchArea)[building];
      relation(area.searchArea)[building];
    );
    out center;
    """
    
    # Query to retrieve townhall coordinates within the city
    townhall_query = f"""
    [out:json];
    area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_id}]->.searchArea;
     (
        node(area.searchArea)[place~"city|town|village"];
        way(area.searchArea)[place~"city|town|village"];
        relation(area.searchArea)[place~"city|town|village"];
    );
    out body;
    """
    
    # Send requests to Overpass API
    building_response = requests.get(overpass_url, params={"data": building_query})
    townhall_response = requests.get(overpass_url, params={"data": townhall_query})
    
    # Parse JSON responses
    building_data = building_response.json()
    townhall_data = townhall_response.json()
    
    # Extract building and townhall coordinates
    building_coords = []
    for element in building_data["elements"]:
        if element["type"] == "node":
            building_coords.append((element["lat"], element["lon"]))
        elif element["type"] == "way" or element["type"] == "relation":
            building_coords.append((element["center"]["lat"], element["center"]["lon"]))
    
    townhall_coord = None
    for element in townhall_data["elements"]:
        if element["type"] == "node":
            townhall_coord = (element["lat"], element["lon"])
            break
        elif element["type"] == "way" or element["type"] == "relation":
            townhall_coord = (element["center"]["lat"], element["center"]["lon"])
            break
    
    if not building_coords or not townhall_coord:
        print(f"No buildings or townhall found in {bfs_id}")
        return None
    
    # Calculate distances using Haversine formula
    distances = []
    for building_coord in building_coords:
        lat1, lon1 = building_coord
        lat2, lon2 = townhall_coord
        
        # Convert coordinates from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = 6371 * c  # Radius of the Earth in kilometers
        
        distances.append(distance)
    
    # Calculate average distance
    avg_distance = sum(distances) / len(distances)
    
    return avg_distance


def get_border_coords(country_code):
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query to retrieve country border coordinates
    border_query = f"""
    [out:json];
    relation["ISO3166-1"="{country_code}"]["admin_level"="2"];
    out geom;
    """
    
    # Send request to Overpass API
    border_response = requests.get(overpass_url, params={"data": border_query})
    
    # Parse JSON response
    border_data = border_response.json()
    
    # Extract country border coordinates
    border_coords = []
    for element in border_data["elements"]:
        if element["type"] == "relation":
            for member in element["members"]:
                if member["type"] == "way":
                    for node in member["geometry"]:
                        border_coords.append((node["lat"], node["lon"]))
    
    return border_coords



def get_distance_to_border(bfs_id: int, border_coords) -> float:
    """
    Get the distance from the city center to the nearest border of the country
    :param bfs_id: BFS ID
    :param border_coords: List of border coordinates
    :return: Distance to the nearest border in kilometers
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query to retrieve city center coordinates
    city_query = f"""
    [out:json];
    area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_id}]->.searchArea;
    (
        node(area.searchArea)[place~"city|town|village"];
        way(area.searchArea)[place~"city|town|village"];
        relation(area.searchArea)[place~"city|town|village"];
    );
    out center;
    """
    
    # Send request to Overpass API
    city_response = requests.get(overpass_url, params={"data": city_query})
    
    # Parse JSON response
    city_data = city_response.json()
    
    # Extract city center coordinates
    city_center = None
    for element in city_data["elements"]:
        if element["type"] == "node":
            city_center = (element["lat"], element["lon"])
            break
        elif element["type"] == "way" or element["type"] == "relation":
            city_center = (element["center"]["lat"], element["center"]["lon"])
            break
    
    if not city_center or not border_coords:
        print(f"City center or country border not found for {bfs_id}")
        return None
    
    # Calculate minimum distance using Haversine formula
    min_distance = float("inf")
    for border_coord in border_coords:
        lat1, lon1 = city_center
        lat2, lon2 = border_coord
        
        # Convert coordinates from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula and https://en.wikipedia.org/wiki/Haversine_formula

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = 6371 * c  # Radius of the Earth in kilometers
        
        min_distance = min(min_distance, distance)
    
    return min_distance
def get_commune_area(bfs_nummer):
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query to retrieve commune boundary
    commune_query = f"""
    [out:json];
    relation[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_nummer}]->.commune;
    (
      way(r.commune);
      node(w);
    );
    out;
    """
    
    # Query to retrieve water bodies within the commune
    water_query = f"""
    [out:json];
    area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_nummer}]->.searchArea;
    (
      way(area.searchArea)[natural="water"];
      relation(area.searchArea)[natural="water"];
      node(w);
    );
    out;
    """
    
    # Send requests to Overpass API
    commune_response = requests.get(overpass_url, params={"data": commune_query})
    water_response = requests.get(overpass_url, params={"data": water_query})
    
    # Parse JSON responses
    commune_data = commune_response.json()
    water_data = water_response.json()
    
    # Extract commune boundary nodes
    commune_nodes = {}
    for element in commune_data["elements"]:
        if element["type"] == "node":
            commune_nodes[element["id"]] = (element["lat"], element["lon"])
    
    # Extract commune boundary geometry from way members
    commune_geometry = []
    for element in commune_data["elements"]:
        if element["type"] == "way":
            for node_id in element["nodes"]:
                if node_id in commune_nodes:
                    commune_geometry.append(commune_nodes[node_id])
    
    # Extract water body nodes
    water_nodes = {}
    for element in water_data["elements"]:
        if element["type"] == "node":
            water_nodes[element["id"]] = (element["lat"], element["lon"])
    
    # Extract water body geometries
    water_geometries = []
    for element in water_data["elements"]:
        if element["type"] == "way":
            geometry = []
            for node_id in element["nodes"]:
                if node_id in water_nodes:
                    geometry.append(water_nodes[node_id])
            water_geometries.append(geometry)
    
    if not commune_geometry:
        print(f"Commune boundary not found for BFS_NUMMER {bfs_nummer}")
        return None, None
    
    # Calculate commune area using polygon area formula
    commune_area = 0
    for i in range(len(commune_geometry)):
        j = (i + 1) % len(commune_geometry)
        commune_area += commune_geometry[i][0] * commune_geometry[j][1] - commune_geometry[j][0] * commune_geometry[i][1]
    commune_area = abs(commune_area) / 2
    
    # Calculate water area using polygon area formula
    water_area = 0
    for geometry in water_geometries:
        for i in range(len(geometry)):
            j = (i + 1) % len(geometry)
            water_area += geometry[i][0] * geometry[j][1] - geometry[j][0] * geometry[i][1]
    water_area = abs(water_area) / 2
    
    return commune_area, water_area