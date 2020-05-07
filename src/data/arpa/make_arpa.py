# -*- coding: utf-8 -*-
import argparse
import os
import logging
import pandas as pd
import sys
import warnings

sys.path.append(os.getcwd())
warnings.filterwarnings('ignore')

from src.data.arpa.arpa_quality_raw_funcs import ArpaConnect, get_all_sensor_data, save_all_sensor_data
from src.config import ARPA_STATIONS


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--build_history",
                        help="[False] historical data are read from zipped csv instead of prebuilt pickle",
                        required=False, default=False, action="store_true")
    args = parser.parse_args()
    return args.build_history


def make_arpa_dataset(build_historical: bool = False):
    """
    Build sensor air quality data from ARPA open dataset, filtering for a selected city (parameter station below).
    If -h is passed as argument to the script, historical data are read from zipped csv.
    Historical data are downloaded as yearly zipped csv while current year data are obtained via API.
    Both kind of sources are publicly available at [this link](https://www.dati.lombardia.it/stories/s/auv9-c2sj)
    """
    arpa = ArpaConnect()
    all_data_list = []
    for station in ARPA_STATIONS:
        logging.info("Building ARPA data for station {s}".format(s=station))
        try:
            station_sensor_df = get_all_sensor_data(arpa=arpa, station=station, build_historical=build_historical)
        except RuntimeError as re:
            logging.exception(re)
            continue
        logging.info("max observation: {}".format(station_sensor_df['data'].max()))
        all_data_list.append(station_sensor_df)
    all_sensor_df = pd.concat(all_data_list)
    save_all_sensor_data(all_sensor_df=all_sensor_df)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    args = parse_args()

    make_arpa_dataset(args)
