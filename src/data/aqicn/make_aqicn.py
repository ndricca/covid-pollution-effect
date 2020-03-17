# -*- coding: utf-8 -*-
import os
import logging
import sys

sys.path.append(os.getcwd())

from src.data.aqicn.air_quality_raw_to_proc import load_stations_data, save_stations_data


def main():
    logging.info('making final data set from raw data')
    stations_df = load_stations_data()
    save_stations_data(stations_df=stations_df)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
