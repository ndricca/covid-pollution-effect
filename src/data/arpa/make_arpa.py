# -*- coding: utf-8 -*-
import os
import logging
import sys

sys.path.append(os.getcwd())

from src.data.arpa.arpa_quality import ArpaConnect, get_all_sensor_data, save_all_sensor_data
from src.config import WT_STATIONS


def main(build_historical=False):
    arpa = ArpaConnect()
    station = WT_STATIONS[0]
    logging.info("Building ARPA data for station {s}".format(s=station))
    all_sensor_df = get_all_sensor_data(arpa=arpa, station=station, build_historical=build_historical)
    save_all_sensor_data(all_sensor_df=all_sensor_df)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    hist_flag = True if len(sys.argv) > 1 and sys.argv[1] == '-h' else False

    main(build_historical=hist_flag)
