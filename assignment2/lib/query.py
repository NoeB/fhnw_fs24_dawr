def get_crosswalk_count(bfs_id: int) -> str:
    """
    Get the number of crosswalks in a given area
    :param bfs_id: BFS ID
    :return: Overpass QL query
    """

    query = f"""
    [out:json][timeout:2];
    area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_id}]->.searchArea;
    (
      node["highway"="crossing"](area.searchArea);
      way["highway"="crossing"](area.searchArea);
      relation["highway"="crossing"](area.searchArea);
    );
    out count;
    """

    return query


def get_traffic_signals_count(bfs_id: int)-> str:
    """
    Get the number of traffic signals in a given area
    :param bfs_id: BFS ID
    :return: Overpass QL query
    """

    query = f"""
            [out:json][timeout:2];

            area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_id}]->.searchArea;
            (
              node(area.searchArea)["highway"="traffic_signals"];
              
            );
            out count;
    """
    return query


def get_house_count(bfs_id: int) -> str:
    """
    Get the number of houses in a given area
    :param bfs_id: BFS ID
    :return: Overpass QL query
    """

    query = f"""
            [out:json][timeout:2];

            area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_id}]->.searchArea;
            (
              way(area.searchArea)["building"="house"];
            );
            out count;
    """
    return query


def get_appartment_count(bfs_id: int) -> str:
    """
    Get the number of appartments in a given area
    :param bfs_id: BFS ID
    :return: Overpass QL query
    """

    query = f"""
            [out:json][timeout:2];

            area[admin_level=8]["swisstopo:BFS_NUMMER"={bfs_id}]->.searchArea;
            (
              way(area.searchArea)["building"="apartments"];
            );
            out count;
    """
    return query

