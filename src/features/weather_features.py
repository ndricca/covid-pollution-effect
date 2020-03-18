# -*- coding: utf-8 -*-
import os
import logging
import sys
import pandas as pd

sys.path.append(os.getcwd())

from src.config import PROC_DATA_DIR


def load_weather_data() -> pd.DataFrame:
    """ Load processed weather data. """
    weather_df = pd.read_pickle(os.path.join(PROC_DATA_DIR, 'weather_data.pkl'))
    return weather_df


def create_weather_events(weather_df: pd.DataFrame) -> pd.DataFrame:
    """ Create binary variables from string containing concatenation of weather events such as rain or snow. """
    weather_list = weather_df['fenomeni'].unique().tolist()
    weather_string = " ".join([e for e in weather_list if isinstance(e, str)])
    weather_events = set(weather_string.split())
    for event in weather_events:
        logging.info("Creating weather event {}".format(event))
        weather_df[event] = weather_df['fenomeni'].str.contains(event, na=False).astype(int)
    return weather_df


if __name__ == '__main__':
    print("ok")
