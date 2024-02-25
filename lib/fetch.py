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