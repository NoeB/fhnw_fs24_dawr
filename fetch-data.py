import os
import requests
from io import BytesIO
from typing import TypedDict, Dict, Optional, List, Set
import lib.fetch as fetch
import lib.scrape as scrape

data_path = './data'

# Ensure the directory exists
os.makedirs(data_path, exist_ok=True)
os.makedirs(data_path + '/raw', exist_ok=True)
os.makedirs(data_path + '/raw/kanton', exist_ok=True)
os.makedirs(data_path + '/raw/bund', exist_ok=True)





class File(TypedDict):
    url: str
    output_file_name: str
    source: str


files: List[File] = [
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_141.csv', 'output_file_name': 'Berufsschueeler.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/39@statistisches-amt-kanton-zuerich'},
    {'url': 'https://www.web.statistik.zh.ch/ogd/daten/ressourcen/KTZH_00002042_00004083.csv', 'output_file_name': 'Einbrueche.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/2042@kantonspolizei-kanton-zuerich'},
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_820.csv', 'output_file_name': 'Unfaelle.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/393@statistisches-amt-kanton-zuerich'}, 
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_400.csv', 'output_file_name': 'DistanzZurNächstenHaltestelle.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/182@statistisches-amt-kanton-zuerich'}, 
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_274.csv', 'output_file_name': 'SteuerKraftProKopf.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/139@statistisches-amt-kanton-zuerich'}, 
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_269.csv', 'output_file_name': 'Schafe.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/118@statistisches-amt-kanton-zuerich'}, 
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_97.csv', 'output_file_name': 'GeburtenRate.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/222@statistisches-amt-kanton-zuerich'}, 
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_133.csv', 'output_file_name':'Bevoekerung.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/204@statistisches-amt-kanton-zuerich'},
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_373.csv', 'output_file_name':'Leerwohnungsquote.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/110@statistisches-amt-kanton-zuerich'},
    #{'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_477.csv', 'output_file_name':'BaulandPreisMedian.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/332@statistisches-amt-kanton-zuerich'},
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_431.csv', 'output_file_name':'NettoVermögen.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/173@statistisches-amt-kanton-zuerich'},
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_305.csv', 'output_file_name':'RestaurantPro1000.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/275@statistisches-amt-kanton-zuerich'},

]


for file in files:
    fetch.download_file_from_url(file['url'], data_path + '/raw/kanton', file['output_file_name'])



# Scrape Table with communes from BFS (Bundesamt für Statistik) and save it to a csv file
# Date is set to 2021, because some it is the most recent year with complete data
scrape.scrape_table_to_csv('https://www.agvchapp.bfs.admin.ch/de/communes/results?EntriesFrom=01.01.2021&EntriesTo=31.12.2021&Canton=ZH', data_path + '/raw/bund', 'gemeinde.csv')