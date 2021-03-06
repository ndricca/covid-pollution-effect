# -*- coding: utf-8 -*-
import os
import logging
import sys

import pandas as pd

from src.config import PROC_DATA_DIR

sys.path.append(os.getcwd())

from src.features.arpa_features import load_arpa_data, filter_by_frequency, aggregate_to_daily
from src.features.weather_features import load_weather_data


def create_dataset(use_daily: bool = None) -> pd.DataFrame:
    """
    Create a dataset with all ARPA air quality data with daily or hourly frequency depending on the argument.
    Weather data are merged by timestamp, assuming that all ARPA data are from the same city of weather data.
    """
    if use_daily is None:
        use_daily = True
    arpa_df = load_arpa_data()
    freq = 'daily' if use_daily else 'hourly'
    freq_arpa_df = filter_by_frequency(arpa_df=arpa_df, freq=freq)
    if freq == 'hourly':
        freq_arpa_df = aggregate_to_daily(arpa_df=arpa_df)
    weather_df = load_weather_data()
    dataset = pd.merge(freq_arpa_df, weather_df, on=['data'])
    return dataset


def save_dataset(dataset: pd.DataFrame):
    """ Save the dataset as pickle """
    out_path = os.path.join(PROC_DATA_DIR, 'dataset.pkl')
    logging.info("saving dataset to {}".format(out_path))
    dataset.to_pickle(out_path)


def load_dataset() -> pd.DataFrame:
    in_path = os.path.join(PROC_DATA_DIR, 'dataset.pkl')
    logging.info("loading dataset from {}".format(in_path))
    dataset = pd.read_pickle(in_path)
    return dataset


def load_normalized_dataset() -> pd.DataFrame:
    in_path = os.path.join(PROC_DATA_DIR, 'normalized_dataset.pkl')
    logging.info("loading normalized dataset from {}".format(in_path))
    dataset = pd.read_pickle(in_path)
    return dataset


if __name__ == '__main__':
    print("ok")
