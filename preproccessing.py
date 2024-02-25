import os
import pandas as pd


data_path = './data'

preprocceced_path = data_path + '/preprocessed'

os.makedirs(preprocceced_path, exist_ok=True)



def load_data(path: str, filename: str = None) -> pd.DataFrame:
    """
    Loads a csv file from the given path and filename

    Keyword arguments:
    path -- the path to the file
    filename -- the name of the file (default None)
    """
    if filename is not None:
        path = os.path.join(path, filename)
    return pd.read_csv(path)



def list_csv_files(path: str) -> list:
    """
    Lists all csv files in the given path

    Keyword arguments:
    path -- the path to the files
    """
    return [f for f in os.listdir(path) if f.endswith('.csv')]


def debug_print_files_with_wrong_rows(path: str, commune_file: str):
    """
    Function used for debugging
    Prints the files with less or more rows than in the commune file

    Keyword arguments:
    path -- the path to the files
    commune_file -- the full path of the commune file
    """
    commune = load_data(commune_file)
    for file in list_csv_files(path):
        df = load_data(path, file)
        if len(df) != len(commune):
            print(file + ' has ' + str(len(df)) + ' rows, but the commune file has ' + str(len(commune)) + ' rows')

def debug_print_files_with_missing_communes(path: str, commune_file: str):
    """
    Function used for debugging
    Prints the files with missing commune numbers

    Keyword arguments:
    path -- the path to the files
    commune_file -- the full path of the commune file
    """
    commune = load_data(commune_file)
    for file in list_csv_files(path):
        df = load_data(path, file)
        for bfs_column in possible_bfs_columns:
            if bfs_column in df.columns:
                missing_comunes = commune[~commune['BFS-Gde Nummer'].isin(df[bfs_column])]['BFS-Gde Nummer']
                if len(missing_comunes) > 0:
                    print(file + ' is missing commune numbers: ' + str(missing_comunes))


# Debugging function which goes through all preprocessed files and checks if the commune numbers are valid (exist in the commune file) prints invalid commune numbers
def debug_list_invalid_comunes(files_path, commune_file: str):
    """
    Function used for debugging
    Lists all invalid commune numbers

    Keyword arguments:
    files_path -- the path to the files
    commune_file -- the full path of the commune file
    """
    commune = load_data(commune_file)
    for file in list_csv_files(files_path):
        df = load_data(files_path, file)
        for bfs_column in possible_bfs_columns:
            if bfs_column in df.columns:
                invalid_comunes = df[~df[bfs_column].isin(commune['BFS-Gde Nummer'])][bfs_column].unique()
                if len(invalid_comunes) > 0:
                    print(file + ' has invalid commune numbers: ' + str(invalid_comunes))

def filter_by_year(df: pd.DataFrame, year: int, possible_year_columns: list) -> pd.DataFrame:
    """
    Filters a DataFrame based on the year

    Keyword arguments:
    df -- the DataFrame to filter
    year -- the year to filter by
    possible_year_columns -- list of possible column names for the year
    """
    for year_column in possible_year_columns:
        if year_column in df.columns:
            return df[df[year_column] == year]
    return df


# How does the tilde look: ~
def filter_out_invalid_comunes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters out invalid communes from the DataFrame

    Keyword arguments:
    df -- the DataFrame to filter
    """
    for bfs_column in possible_bfs_columns:
        if bfs_column in df.columns:
            return df[~df[bfs_column].isin([0,291])]
    return df


## retrun all communen numbers from the file
def get_all_comunen_numbers(filename: str) -> set:
    """
    Returns all commune numbers from the DataFrame

    Keyword arguments:
    filename -- the name of the file
    """
    df = load_data(data_path + '/raw/bund/', filename)
    return set(df['BFS-Gde Nummer'])



possible_year_columns= ['Ausgangsjahr', 'INDIKATOR_JAHR']
possible_bfs_columns = ['BFS_NR', 'Gemeinde_BFS_Nr']
possible_bfs_numbers = get_all_comunen_numbers('gemeinde.csv')


# Filter common invalid rows out 
for file in list_csv_files(data_path + '/raw/kanton'):
    df = load_data(data_path + '/raw/kanton', file)
    df = filter_by_year(df, 2021, possible_year_columns)
    df = filter_out_invalid_comunes(df)
    df.to_csv(preprocceced_path + '/' + file, index=False)

# Filter out rows out of einbrüche file
einbrueche_df = load_data(preprocceced_path + '/Einbrueche.csv')
einbrueche_df = einbrueche_df[einbrueche_df['Tatbestand'] == 'Einbrüche insgesamt']
einbrueche_df = einbrueche_df[einbrueche_df['Gemeinde_BFS_Nr'].isin(possible_bfs_numbers)]
einbrueche_df = einbrueche_df.groupby('Gemeinde_BFS_Nr').agg({'Straftaten_total': 'sum', 'Straftaten_vollendet': 'sum', 'Straftaten_versucht': 'sum', 'Einwohner': 'sum', 'Häufigkeitszahl': 'mean'}).reset_index()
einbrueche_df.to_csv(preprocceced_path + '/Einbrueche.csv', index=False)



debug_print_files_with_wrong_rows(preprocceced_path, './data/raw/bund/gemeinde.csv')
debug_list_invalid_comunes(preprocceced_path, './data/raw/bund/gemeinde.csv')
debug_print_files_with_missing_communes(preprocceced_path, './data/raw/bund/gemeinde.csv')