import requests

def get_accidents_count(bfs_id: int) -> int:
    """
    Get the number of accidents in a given area
    :param bfs_id: BFS ID
    :return: Number of accidents
    """
    url = f"https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.astra.unfaelle-personenschaeden_alle&searchText={bfs_id}&searchField=fsocommunecode&returnGeometry=false"
    response = requests.get(url)
    data = response.json()
    # Count array length
    return len(data['results'])
