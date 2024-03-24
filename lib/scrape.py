import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO



def scrape_table_to_csv(url: str, dir_path: str, output_file_name: str = None, multiple_tables=False):
    """
    Scrape a table from a webpage and save it to a csv file
    :param url: URL of the webpage
    :param dir_path: Directory to extract the file to
    :param output_file_name: Name of the file to save as
    :param multiple_tables: If the webpage has multiple tables
    """
    # Load the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the tables
    
   
    tables = soup.find_all('table')[0:1]
    if multiple_tables:
         tables = soup.find_all('table')
    df = pd.DataFrame()

    for i, table in enumerate(tables):
        #find the table
        table = soup.find_all('table')[i]
        # Convert the table to a dataframe
        table_df = pd.read_html(StringIO(str(table)))[0]
        df = pd.concat([df, table_df], ignore_index=True)



    # Save the dataframe to a csv file
    df.to_csv(dir_path + '/' + output_file_name, index=False)

    print('Download complete')