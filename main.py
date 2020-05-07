import argparse
import logging

from src.data.arpa.make_arpa import make_arpa_dataset
from src.data.make_dataset import make_dataset
from src.data.weather.make_weather import make_weather_dataset
from src.models.normalize_weather import predict_normalized_pollutant


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--build_history",
                        help="[False] historical data are read from zipped csv instead of prebuilt pickle",
                        required=False, default=False, action="store_true")
    parser.add_argument("-d", "--daily",
                        help="[False] daily data are considered instead of hourly",
                        required=False, default=False, action="store_true")
    args = parser.parse_args()
    parms = {
        "build_historical": args.build_history,
        "use_daily": args.daily
    }
    return parms


def main(build_historical: bool, use_daily: bool, **kwargs):
    make_arpa_dataset(build_historical=build_historical)
    make_weather_dataset()
    # make_dataset(use_daily=use_daily)
    # predict_normalized_pollutant()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    # FIXME: understand why log format is not correctly displayed
    try:
        parameters = parse_args()
        logging.info("Executing updating pipeline")
        main(**parameters)
    except Exception as e:
        logging.exception(e)
