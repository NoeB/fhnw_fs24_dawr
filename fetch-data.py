import os
import pandas as pd
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
os.makedirs(data_path + '/raw/wikipedia', exist_ok=True)




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
   # {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_477.csv', 'output_file_name':'BaulandPreisMedian.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/332@statistisches-amt-kanton-zuerich'}, // For now exluded because of missing data
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_431.csv', 'output_file_name':'NettoVermögen.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/173@statistisches-amt-kanton-zuerich'},
    {'url': 'https://www.web.statistik.zh.ch/ogd/data/KANTON_ZUERICH_305.csv', 'output_file_name':'RestaurantPro1000.csv', 'source': 'https://www.zh.ch/de/politik-staat/statistik-daten/datenkatalog.html#/datasets/275@statistisches-amt-kanton-zuerich'},

]


for file in files:
    fetch.download_file_from_url(file['url'], data_path + '/raw/kanton', file['output_file_name'])



# Scrape Table with communes from BFS (Bundesamt für Statistik) and save it to a csv file
# Date is set to 2021, because some it is the most recent year with complete data
scrape.scrape_table_to_csv('https://www.agvchapp.bfs.admin.ch/de/communes/results?EntriesFrom=01.01.2021&EntriesTo=31.12.2021&Canton=ZH', data_path + '/raw/bund', 'gemeinde.csv')

#https://dumps.wikimedia.org/dewiki/latest/
#https://www.zh.ch/de/suche/_jcr_content/searchoverview.zhweb-search.json?fullText=Andelfingen&noAutoCorrection=false

# go through all geimeinde and  execute search on Kanton Zürich website by Gemeindename file location: data_path + '/raw/bund', 'gemeinde.csv'
gemeinde = pd.read_csv(data_path + '/raw/bund/gemeinde.csv')

kanton_matches_by_commune = []

for index, row in gemeinde.iterrows():
    # Remove (ZH) from Gemeindename
    row['Gemeindename'] = row['Gemeindename'].replace(' (ZH)', '')
    search = fetch.search_kanton_zurich_by_keyword(row['Gemeindename'])

    new_row = {'Gemeindename': row['Gemeindename'], 'BFS_NR': row['BFS-Gde Nummer'], 'matches': search['resultsData']['numberOfResults']}
    kanton_matches_by_commune.append(new_row)

kanton_matches_by_commune_df = pd.DataFrame(kanton_matches_by_commune) 
kanton_matches_by_commune_df.to_csv(data_path + '/raw/kanton/kanton_matches_by_commune.csv', index=False)



# Grep all gemeinde names and fetch Wikipedia pageviews for them https://als.wikipedia.org/wiki/Gemeinden_des_Kantons_Zürich
scrape.scrape_table_to_csv('https://als.wikipedia.org/wiki/Gemeinden_des_Kantons_Zürich', data_path + '/raw/wikipedia', 'gemeinde_wikipedia.csv', multiple_tables=True)

# Join Wikipedia pageviews with gemeinde and join on Gemeindename and Gemeindename
gemeinde = pd.read_csv(data_path + '/raw/bund/gemeinde.csv')
wiki_names = pd.read_csv(data_path + '/raw/wikipedia/gemeinde_wikipedia.csv').dropna(subset=['Offiziell Name vo dr Gmäind'])

merged_wiki = pd.merge(gemeinde, wiki_names, left_on='Gemeindename', right_on='Offiziell Name vo dr Gmäind', how='left')

# Go thorugh all merged rows and check if 'Offiziell Name vo dr Gmäind' is null
# If its null try to find the gemeinde if the name is adapted (some gemeinde have a ZH appendix or are missing the appendix)
for index, row in merged_wiki.iterrows():
    if pd.isnull(row['Offiziell Name vo dr Gmäind']):
        name = row['Gemeindename'].replace(' (ZH)', '').replace(' ZH', '')
        # Find if the name is in the wiki_names
        if wiki_names['Offiziell Name vo dr Gmäind'].replace(' ZH', '').str.contains(name).any():
            # Get Wiki Row with the name
            wiki_row  = wiki_names[wiki_names['Offiziell Name vo dr Gmäind'].replace(' ZH', '').str.contains(name)]
            # Merge the row with the wiki_names
            merged_wiki.loc[index, 'Offiziell Name vo dr Gmäind'] = wiki_row['Offiziell Name vo dr Gmäind'].values[0]



# Stammheim is mising in the wikipedia tables  therefor I must add the pageviews manually
merged_wiki.loc[merged_wiki['Gemeindename'] == 'Stammheim', 'Offiziell Name vo dr Gmäind'] = 'Stammheim ZH'           
# Schlatt has a different name in the wikipedia table
merged_wiki.loc[merged_wiki['Gemeindename'] == 'Schlatt (ZH)', 'Offiziell Name vo dr Gmäind'] = 'Schlatt ZH'


merged_wiki = merged_wiki[['BFS-Gde Nummer', 'Gemeindename', 'Offiziell Name vo dr Gmäind']]
# Rename columns
merged_wiki.columns = ['BFS_NR', 'Gemeindename', 'CH_Gemeindename_wikipedia']

# Get Pageviews for all comunes and save it to a csv file
for index, row in merged_wiki.iterrows():
    search = fetch.fetch_wikipedia_pageviews(row['CH_Gemeindename_wikipedia'].replace(' ', '_'), 2021)
    merged_wiki.loc[index, 'pageviews'] = search

merged_wiki.to_csv(data_path + '/raw/wikipedia/wiki_pageviews.csv', index=False)




#Source: https://app.statistik.zh.ch/wahlen_abstimmungen/prod/Archive/Det/1_1_20211128/222432/Abstimmungen/Resultate
fetch.download_file_from_url('https://pstwahlenabstimmungen01.z1.web.core.windows.net/data_prod/geschaefte/1_1_20211128/2021_11_28_resultate_zh.xls', data_path + '/raw/kanton', 'abstimmung.xls')
