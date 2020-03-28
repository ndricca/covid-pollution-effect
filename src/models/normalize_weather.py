# -*- coding: utf-8 -*-
import os
import logging
import sys

sys.path.append(os.getcwd())

from src.models.train_model import pipeline_normalize_multi_sensors


def main(use_daily: bool = None):
    """
    Build total dataset merging ARPA air quality data with weather data.
    If -h is passed as argument to the script, only hourly ARPA data are filtered, otherwise daily data are selected.
    """
    logging.info('normalize all sensors available into dataset')
    pipeline_normalize_multi_sensors()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
