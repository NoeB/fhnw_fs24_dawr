import requests
from io import BytesIO


def download_file_from_url(url: str, dir_path: str, output_file_name: str = None):
    """
    Download a file from a URL and save it to a directory
    :param url: URL to download the file from
    :param dir_path: Directory to extract the file to
    :param output_file_name: Name of the file to save as
    """
    print('Downloading file from: ' + url)
    response = requests.get(url)
    file = BytesIO(response.content)
    if output_file_name is None:
        output_file_name = url.split('/')[-1]
    with open(dir_path + '/' + output_file_name, 'wb') as f:
        f.write(file.getbuffer())
    print('Download complete')


def search_kanton_zurich_by_keyword(keyword: str):
    """
    Execute search on Kanton Zürich website by keyword
    :param keyword: Keyword to search for
    :return: JSON response from the search
    """
    print('Searching Kanton Zürich website for keyword: ' + keyword)
    response = requests.get('https://www.zh.ch/de/suche/_jcr_content/searchoverview.zhweb-search.json?fullText=' + keyword + '&noAutoCorrection=false')
    return response.json()


def fetch_wikipedia_pageviews(page: str, year: int) -> int:
    """
    Fetch pageviews for a Wikipedia page in alemannische
    :param page: Name of the Wikipedia page
    :param year: Year to fetch pageviews for
    :return count per year
    """
    print('Fetching Wikipedia pageviews for page: ' + page + ' in year: ' + str(year))
    # Add user agent to request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    views = 0
    response = requests.get('https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/als.wikipedia/all-access/all-agents/' + page + '/monthly/' + str(year) + '0101/' + str(year) + '1231', headers=headers)
    if response.status_code != 200:
        return views
    response = response.json()
    for item in response['items']:
        views += item['views']

    return views

    
        