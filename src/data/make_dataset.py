# -*- coding: utf-8 -*-
import os
import logging
import sys
import pandas as pd

sys.path.append(os.getcwd())

from src.config import PROC_DATA_DIR



def load_arpa_data():
    arpa_df = pd.read_csv(os.path.join(PROC_DATA_DIR, 'arpa_data.csv'))
    return arpa_df


def load_weather_data():
    weather_df = pd.read_csv(os.path.join(PROC_DATA_DIR, 'weather_data.csv'))
    return weather_df

def main():
    logging.info('making final data set from raw data')
    pass


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
