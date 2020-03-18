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


if __name__ == '__main__':
    print("ok")
