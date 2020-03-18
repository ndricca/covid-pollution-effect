# -*- coding: utf-8 -*-
import os
import logging
import sys

import pandas as pd

sys.path.append(os.getcwd())

from src.data.common_funcs import create_dataset, save_dataset


def main(use_daily: bool = None):
    """
    Build total dataset merging ARPA air quality data with weather data.
    If -h is passed as argument to the script, only hourly ARPA data are filtered, otherwise daily data are selected.
    """
    logging.info('making final dataset from raw data')
    dataset = create_dataset(use_daily=use_daily)
    save_dataset(dataset=dataset)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    if len(sys.argv)>1 and sys.argv[1] == '-h':
        use_daily = False
    else:
        use_daily = True
    main(use_daily=use_daily)
