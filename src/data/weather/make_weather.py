import os
import logging
import sys

sys.path.append(os.getcwd())

from src.data.weather.weather_raw_to_proc import download_weather_data, create_weather_df, save_weather_df  # NOQA


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    download_weather_data()
    weather_df = create_weather_df()
    save_weather_df(weather_df=weather_df)
