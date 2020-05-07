import argparse
import os
import logging
import sys

sys.path.append(os.getcwd())

from src.data.weather.weather_raw_funcs import download_weather_data, create_weather_df, save_weather_df


def parse_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args


def make_weather_dataset():
    """
    Build weather data extracted from [this link](https://www.ilmeteo.it/portale/archivio-meteo/).
    Current month data are always downloaded, while previous month are downloaded only if absent from directory.
    """
    download_weather_data()
    weather_df = create_weather_df()
    logging.info("max observation: {}".format(weather_df['data'].max()))
    save_weather_df(weather_df=weather_df)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    _ = parse_args()
    make_weather_dataset()
