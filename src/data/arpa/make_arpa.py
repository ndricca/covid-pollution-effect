# -*- coding: utf-8 -*-
import os
import logging
import sys

sys.path.append(os.getcwd())

from src.data.arpa.arpa_quality import ArpaConnect, get_all_sensor_data, save_all_sensor_data  # NOQA
from src.config import WT_STATIONS  # NOQA


def main(build_historical: bool = False):
    """
    Build sensor air quality data from ARPA open dataset, filtering for a selected city (parameter station below).
    If -h is passed as argument to the script, historical data are read from zipped csv.
    Historical data are downloaded as yearly zipped csv while current year data are obtained via API.
    Both kind of sources are publicly available at [this link](https://www.dati.lombardia.it/stories/s/auv9-c2sj)
    """
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
