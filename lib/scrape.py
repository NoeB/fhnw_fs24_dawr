import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO



def scrape_table_to_csv(url: str, dir_path: str, output_file_name: str = None):
    """
    Scrape a table from a webpage and save it to a csv file
    :param url: URL of the webpage
    :param dir_path: Directory to extract the file to
    :param output_file_name: Name of the file to save as
    """
    # Load the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table
    table = soup.find_all('table')[0]

    # Convert the table to a dataframe
    df = pd.read_html(StringIO(str(table)))[0]

    # Save the dataframe to a csv file
    df.to_csv(dir_path + '/' + output_file_name, index=False)

    print('Download complete')