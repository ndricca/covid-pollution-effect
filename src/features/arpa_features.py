# -*- coding: utf-8 -*-
import os
import logging
import sys
import pandas as pd

sys.path.append(os.getcwd())

from src.config import PROC_DATA_DIR, ARPA_MEASURES_FREQ


def load_arpa_data() -> pd.DataFrame:
    """ Load processed dataframe. """
    logging.info("loading processed air quality ARPA data")
    arpa_df = pd.read_pickle(os.path.join(PROC_DATA_DIR, 'arpa_data.pkl'))
    return arpa_df


def filter_by_frequency(arpa_df: pd.DataFrame, freq: str = None) -> pd.DataFrame:
    """ Filter sensor dataframe by time frequency """
    if freq is None:
        freq = 'daily'
    logging.info("selecting sensor data with {f} frequency".format(f=freq))
    freq_arpa_df = arpa_df.loc[arpa_df['nometiposensore'].isin(ARPA_MEASURES_FREQ[freq])]
    return freq_arpa_df


def aggregate_to_daily(arpa_df: pd.DataFrame) -> pd.DataFrame:
    order_cols = list(arpa_df.columns)
    hourly_arpa_df = arpa_df.rename({'data': 'data_ora'}, axis=1)
    hourly_arpa_df['data'] = hourly_arpa_df['data_ora'].astype('<M8[D]')
    daily_arpa_df = hourly_arpa_df.groupby(['idsensore', 'data', 'nometiposensore', 'idstazione']).agg(
        {'valore': 'mean', 'stato': 'first'}).reset_index()
    return daily_arpa_df[order_cols]


if __name__ == '__main__':
    print("ok")
