# -*- coding: utf-8 -*-
import argparse
import os
import logging
import sys
import warnings

sys.path.append(os.getcwd())
warnings.filterwarnings('ignore')

from src.data.common_funcs import create_dataset, save_dataset


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--daily",
                        help="[False] daily data are considered instead of hourly",
                        required=False, default=False, action="store_true")
    args = parser.parse_args()
    return args.daily


def make_dataset(use_daily: bool = None):
    """
    Build total dataset merging ARPA air quality data with weather data.
    If use_daily is passed as argument, only daily ARPA data are filtered, otherwise hourly data are selected.
    """
    logging.info('making final dataset from raw data')
    dataset = create_dataset(use_daily=use_daily)
    logging.info("max observation: {}".format(dataset['data'].max()))
    save_dataset(dataset=dataset)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    daily = parse_args()
    make_dataset(use_daily=daily)
