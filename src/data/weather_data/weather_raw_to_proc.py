import datetime
import logging
import os
import pandas as pd
import requests
import sys

sys.path.append(os.getcwd())

from src.config import WT_BASE_URL, ITA_MONTHS, WT_DATA_DIR, WT_STATIONS, WT_START_YEAR, PROC_DATA_DIR


def download_weather_month(station: str = 'Milano', year: str = None, month: str = None):
    """
    Download csv file for selected station, year and month.
    Year and month are expected to be string such as '2020' and '03', respectively.
    """
    if year is None:
        year = str(datetime.datetime.now().year)
    if month is None:
        month = str(datetime.datetime.now().strftime("%m"))
    ita_month = ITA_MONTHS[month]
    weather_url = WT_BASE_URL + "/".join([station, year, ita_month]) + "?format=csv"
    res = requests.get(weather_url)
    weather_out_path = os.path.join(WT_DATA_DIR, 'weather_{}.csv'.format("_".join([station, year, ita_month])))
    logging.info("downloading data for {s} {y} {m} to {p}".format(s=station, y=year, m=ita_month, p=weather_out_path))
    with open(weather_out_path, 'w') as f, requests.get(weather_url, stream=True) as r:
        decoded = r.content.decode('ANSI')
        f.write(decoded)


def _get_year_month(file_name):
    """
    Extract year and month from file name and concatenate to year-month string
    """
    ym = file_name.replace('.csv', '')
    year, ita_month = ym.split("_")[-2:]
    month = [k for k, v in ITA_MONTHS.items() if v == ita_month][0]
    return year + "-" + month


def get_params_list(start_year: str = None, stations_list: list = None) -> list:
    """
    Calculate all combinations of parameters to be retrieved online.
    """
    if start_year is None:
        start_year = WT_START_YEAR
    if stations_list is None:
        stations_list = WT_STATIONS
    files_to_download = []
    start_year_month = start_year + "-01"
    curr_year_month = str(datetime.datetime.now().strftime('%Y-%m'))
    downloaded_files = os.listdir(WT_DATA_DIR)
    downloaded_year_months = [_get_year_month(f) for f in downloaded_files if _get_year_month(f) != curr_year_month]
    for station in stations_list:
        for ym in pd.date_range(start_year_month, curr_year_month, freq='MS'):
            if ym.strftime('%Y-%m') not in downloaded_year_months:
                params_dict = {}
                params_dict['station'] = station
                params_dict['year'] = str(ym.year)
                params_dict['month'] = ym.strftime('%m')
                files_to_download.append(params_dict)
    return files_to_download


def download_weather_data():
    params_list = get_params_list()
    for params_dict in params_list:
        download_weather_month(**params_dict)


def _clean_cols(c_name):
    cleaned = c_name.replace('°C', 'celsius')
    cleaned = cleaned.replace('%', 'perc')
    cleaned = cleaned.replace('/', '')
    cleaned = cleaned.lower().lstrip().rstrip()
    return cleaned


def create_weather_df(data_dir: str = None) -> pd.DataFrame:
    if data_dir is None:
        data_dir = WT_DATA_DIR
    files = os.listdir(data_dir)
    weather_df = pd.concat([pd.read_csv(os.path.join(data_dir, f), sep=';', parse_dates=['DATA']) for f in files])
    weather_df.columns = [_clean_cols(c) for c in weather_df.columns]
    return weather_df


def save_weather_df(weather_df: pd.DataFrame, output_proc_file: str = None):
    if output_proc_file is None:
        output_proc_file = 'weather_data.csv'
    path_to_output = os.path.join(PROC_DATA_DIR, output_proc_file)
    logging.info("saving weather dataframe as csv in {f}".format(f=output_proc_file))
    weather_df.to_csv(path_to_output, index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    download_weather_data()
    weather_df = create_weather_df()
    save_weather_df(weather_df=weather_df)
