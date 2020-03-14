import datetime
import os
import pandas as pd
import logging

from src.config import RAW_DATA_DIR, PROC_DATA_DIR


def _strip_string(string):
    return string.lstrip().rstrip()


def prepare_station_df(station_df: pd.DataFrame, file_name: str) -> pd.DataFrame:
    """
    Prepare the dataframe adding columns with information from file name

    :param station_df: pandas dataframe with station data
    :param file_name: name of the file needed to extract info

    :return: dataframe with date as index,
    """
    station_name, region = file_name.split(',')[:2]
    city = station_name.split('-')[0]
    station_df.columns = [_strip_string(c) for c in station_df.columns]
    prep_station_df = station_df.set_index('date').sort_index()
    station_info = {
        'station_name': _strip_string(station_name),
        'city': _strip_string(city),
        'region': _strip_string(region)
    }
    for k, v in station_info.items():
        prep_station_df[k] = v
    quality_cols = [c for c in prep_station_df.columns if c not in list(station_info.values())]
    return prep_station_df[list(station_info.values()) + quality_cols]


def load_single_station_data(path_to_file: str, file_name: str) -> pd.DataFrame:
    """
    Read the csv and prepare the data adding info from filename

    :param path_to_file: path to the folder
    :param file_name: nome of the file to be loaded

    :return: station dataframe
    """
    logging.info("loading file {s}".format(s=file_name))
    path_to_file_name = os.path.join(path_to_file, file_name)

    station_df = pd.read_csv(path_to_file_name, na_values=' ', parse_dates=['date'])
    station_df = prepare_station_df(station_df=station_df, file_name=file_name)
    return station_df


def load_stations_data(specific_station_file: str = None) -> pd.DataFrame:
    """
    Build a unique dataframe with data from single stations csv files.
    Load only data for a  specified station if it is specified.

    :param specific_station_file: name of the specific station csv file

    :return: pandas dataframe with stations data
    """
    if specific_station_file:
        stations_df = load_single_station_data(path_to_file=RAW_DATA_DIR, file_name=specific_station_file)
    else:
        files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('italy-air-quality.csv')]
        stations_df = pd.DataFrame()
        for file in files:
            station_df = load_single_station_data(path_to_file=RAW_DATA_DIR, file_name=file)
            stations_df = pd.concat([stations_df, station_df])
    return stations_df


def save_stations_data(stations_df: pd.DataFrame, specific_file: str = 'stations_data'):
    """
    Save dataframe to preprocessed folder
    """
    path_to_output = os.path.join(PROC_DATA_DIR, specific_file)
    logging.info("saving stations dataframe as csv in {f}".format(f=specific_file))
    stations_df.to_csv(path_to_output)

