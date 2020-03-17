# -*- coding: utf-8 -*-
import datetime
import os
import pandas as pd
import logging

from src.config import PROC_DATA_DIR, DT_ID_COLS, AQ_COLS


def _series_as_str(column: pd.Series, zfill_len: int = 2) -> pd.Series:
    if zfill_len:
        return column.astype(str).str.zfill(zfill_len)
    else:
        return column.astype(str)


def create_dt_features(stations_df: pd.DataFrame) -> pd.DataFrame:
    """ Build year, month, day, weekday columns and relevant average values"""
    dt_stations_df = stations_df.copy().set_index('date')
    dt_stations_df['year'] = _series_as_str(dt_stations_df.index.year)
    dt_stations_df['month'] = _series_as_str(dt_stations_df.index.month)
    dt_stations_df['year_month'] = dt_stations_df.index.strftime('%Y-%m')
    dt_stations_df['day'] = _series_as_str(dt_stations_df.index.day)
    dt_stations_df['weekofyear'] = _series_as_str(dt_stations_df.index.weekofyear)
    dt_stations_df['wday'] = _series_as_str(dt_stations_df.index.weekday, zfill_len=1)
    return dt_stations_df


def load_air_quality_data(proc_file: str = 'stations_data.csv') -> pd.DataFrame:
    """ Read processed data from csv. Date is parsed as datetime object. """
    path_to_file = os.path.join(PROC_DATA_DIR, proc_file)
    logging.info("loading file {f}".format(f=path_to_file))
    stations_df = pd.read_csv(path_to_file, parse_dates=['date'])
    stations_df = create_dt_features(stations_df=stations_df)
    return stations_df


def get_overall_daily_means(dt_stations_df: pd.DataFrame) -> pd.DataFrame:
    daily_means = dt_stations_df.groupby(DT_ID_COLS)[AQ_COLS].mean().reset_index()
    return daily_means


def year_on_year_comparison(dt_stations_df: pd.DataFrame, station: str = None, curr_year: str = None,
                            comp_year: str = None) -> pd.DataFrame:
    if curr_year is None:
        curr_year = str(datetime.datetime.now().year)
    if comp_year is None:
        comp_year = str(datetime.datetime.now().year - 1)
    if station:
        dt_stations_df = dt_stations_df.loc[dt_stations_df['station_name'] == station]
    curr_df = dt_stations_df.loc[dt_stations_df['year'] == curr_year, DT_ID_COLS + AQ_COLS].reset_index()
    comp_df = dt_stations_df.loc[dt_stations_df['year'] == comp_year, DT_ID_COLS + AQ_COLS].reset_index()
    yoy_df = pd.merge(curr_df, comp_df, on=DT_ID_COLS, how='outer', suffixes=("_" + curr_year, "_" + comp_year))
    yoy_df = yoy_df.rename({'date_' + curr_year: 'date'}, axis=1)
    yoy_df = yoy_df.loc[~yoy_df['date'].isnull()].set_index('date')
    return yoy_df


def plot_year_on_year_comparison(yoy_df: pd.DataFrame, aq_col: str = None, smooth: bool = False):
    if aq_col is None:
        aq_col = AQ_COLS[1]
    yoy_aq_cols = [c for c in yoy_df.columns if c.startswith(aq_col)]
    if smooth:
        plt_yoy = yoy_df[yoy_aq_cols].ewm(span=7, ignore_na=True).mean()
    else:
        plt_yoy = yoy_df[yoy_aq_cols]
    return plt_yoy


if __name__ == '__main__':
    print("ok")
