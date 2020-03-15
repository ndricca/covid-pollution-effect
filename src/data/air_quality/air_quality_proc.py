# -*- coding: utf-8 -*-
import os
import pandas as pd
import logging


from src.config import PROC_DATA_DIR


def load_proc_data(proc_file: str = 'stations_data.csv') -> pd.DataFrame:
    """ Read processed data from csv. Date is parsed as datetime object. """
    path_to_file = os.path.join(PROC_DATA_DIR, proc_file)
    logging.info("loading file {f}".format(f=path_to_file))
    stations_df = pd.read_csv(path_to_file, parse_dates=['date'])
    return stations_df


def _series_as_str(column: pd.Series, zfill_len: int = 2) -> pd.Series:
    if zfill_len:
        return column.astype(str).str.zfill(zfill_len)
    else:
        return column.astype(str)


def create_dt_features(stations_df: pd.DataFrame) -> pd.DataFrame:
    """ Build year, month, day, weekday columns and relevant average values"""
    dt_stations_df = stations_df.copy().set_index('date')
    dt_stations_df['year'] = _series_as_str(dt_stations_df.index.year)
    dt_stations_df['mont'] = _series_as_str(dt_stations_df.index.month)
    dt_stations_df['year_month'] = dt_stations_df.index.strftime('%Y-%m')
    dt_stations_df['day'] = _series_as_str(dt_stations_df.index.month)
    dt_stations_df['wday'] = _series_as_str(dt_stations_df.index.weekday, None)
    return dt_stations_df
