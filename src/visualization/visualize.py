# -*- coding: utf-8 -*-
import datetime
import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

sys.path.append(os.getcwd())

from src.data.common_funcs import load_dataset
from src.config import DEFAULT_PLOTLY_COLORS, DEFAULT_PLOTLY_XAXIS_CFG


def dataset_for_viz():
    dataset = load_dataset()
    return dataset


def dist_values_from_series(series: pd.Series, add_none: str = 'start') -> list:
    """
    Extract unique values from series and return them as a list.
    A default set to None is added if
    """
    params_list = []
    if add_none == 'start':
        params_list += [None]
    params_list += sorted(series.unique().tolist())
    if add_none == 'end':
        params_list += [None]
    return params_list


def create_params_dict(dataset: pd.DataFrame) -> dict:
    params_dict = {}
    params_dict['idsensore'] = dist_values_from_series(dataset['idsensore'], add_none='end')
    params_dict['nometiposensore'] = dist_values_from_series(dataset['nometiposensore'])
    params_dict['idstazione'] = dist_values_from_series(dataset['idstazione'])
    return params_dict


def create_select_box(st: st, params_dict: dict, ph: dict) -> dict:
    for box_name, values in params_dict.items():
        ph[box_name] = st.selectbox(box_name, values)
    return ph


def filter_dates(dataset: pd.DataFrame, start_date: datetime.date) -> pd.DataFrame:
    start_ts = pd.to_datetime(start_date)
    return dataset.loc[dataset['data'] >= start_ts]


def display_vega_scatter(data: pd.DataFrame, weather_info: str, **kwargs):
    if weather_info is None:
        weather_info = 'umidita_perc'
    st.subheader("Scatter plot of {} on pollutant by sensor".format(weather_info))
    vega_args = {
        'mark': 'circle',
        'encoding': {
            'facet': {'field': 'idsensore', 'type': 'nominal', 'columns': 2},
            'x': {'bin': {'maxbins': 50}, 'field': weather_info, 'type': 'quantitative'},
            'y': {'bin': {'maxbins': 50}, 'field': 'valore', 'type': 'quantitative'},
            'color': {'aggregate': 'count', 'type': 'quantitative'}
        },
        "config": {"view": {"stroke": "transparent"}}
    }
    st.vega_lite_chart(data, vega_args)


def display_sensor_scatter(data: pd.DataFrame, weather_info: str, n_col: int = 2, use_st=False, **kwargs):
    if weather_info is None:
        weather_info = 'umidita_perc'
    if use_st:
        st.subheader("Scatter plot of {} on pollutant by sensor".format(weather_info))
    sens_cols = data['idsensore'].unique()
    n_rows = len(sens_cols) // n_col + 1
    plt.figure(figsize=(10, 5))
    for i, (sens, sens_df) in enumerate(data.groupby('idsensore')):
        plt.subplot(n_rows, n_col, i + 1)
        plt.title("Effect of {w} for sensor {i}".format(w=weather_info, i=sens))
        plt.hexbin(sens_df[weather_info], sens_df['valore'], mincnt=1, bins='log', gridsize=40,
                   cmap=plt.get_cmap('Blues'))
    plt.tight_layout()
    if use_st:
        st.pyplot()
    else:
        plt.show()


def display_timestamp(lines: pd.DataFrame, use_st=False):
    for sensor in lines.columns[1:]:
        plt.plot('data', sensor, data=lines, label=sensor)
    plt.legend()
    if use_st:
        st.pyplot()
    else:
        plt.show()


def display_plotly_timestamp(lines: pd.DataFrame, color_only_col: str = '', before_after_areas=False, use_st=False):
    fig = go.Figure()
    value_cols = [c for c in lines.columns if c != 'data']
    for i, line_col in enumerate(value_cols):
        if color_only_col:
            line_color = 'rgb(238,57,57)' if line_col == color_only_col else 'rgb(170,170,170)'
        else:
            line_color = DEFAULT_PLOTLY_COLORS[i]
        fig.add_trace(go.Scatter(
            x=lines['data'],
            y=lines[line_col],
            mode="lines+markers",
            name=line_col,
            line_color=line_color))
    # Use date string to set xaxis range
    fig.update_layout(xaxis=DEFAULT_PLOTLY_XAXIS_CFG)
    if before_after_areas:
        fig.update_layout(
            shapes=[
                # 1st highlight during Jan 15 - Jan 29
                {'type': "rect", 'xref': "x", 'yref': "paper", 'x0': "2020-01-15", 'y0': 0, 'x1': "2020-01-29", 'y1': 1,
                 'fillcolor': "LightSalmon", 'opacity': 0.5, 'layer': "below", 'line_width': 0},
                # 2nd highlight during Mar 01 - Mar 10
                {'type': "rect", 'xref': "x", 'yref': "paper", 'x0': "2020-03-01", 'y0': 0, 'x1': "2020-03-10", 'y1': 1,
                 'fillcolor': "LightGreen", 'opacity': 0.5, 'layer': "below", 'line_width': 0}
            ]
        )
    if use_st:
        st.plotly_chart(fig)
    else:
        fig.show()


def get_yearly_avg(data: pd.DataFrame, year: int, keep_date: bool = False, day_of_year=True) -> pd.DataFrame:
    yrl_data = data.loc[data['data'].dt.year == year]
    if day_of_year:
        yrl_data['date_comp'] = yrl_data['data'].dt.strftime('%m-%d')
    else:
        yrl_data['date_comp'] = yrl_data['data'].dt.strftime('%U-%w')
    if keep_date:
        yrl_avg = yrl_data.groupby(['data', 'date_comp']).mean()['valore']
    else:
        yrl_avg = yrl_data.groupby(['date_comp']).mean()['valore']
    return yrl_avg


def reindex_data(df: pd.DataFrame, dt_as_idx: bool = False, dt_col: str = 'data') -> pd.DataFrame:
    if dt_as_idx:
        df = df.reindex(pd.date_range(df.index.min(), df.index.max(), freq='D'))
    else:
        df = df.set_index(dt_col)
        df = df.reindex(pd.date_range(df.index.min(), df.index.max(), freq='D'))
        df.index.name = dt_col
        df = df.reset_index()
    return df


def summarize_sensors(lines: pd.DataFrame, dt_as_idx: bool = True, dt_col: str = 'data',
                      na_per_sensor: float = None, na_per_date: int = None,
                      method: str = 'median') -> pd.Series:
    if not dt_as_idx:
        try:
            lines = lines.set_index(dt_col)
        except Exception:
            raise IndexError("dt_as_idx has been set to False and impossible to set {c} as index".format(c=dt_col))
    if na_per_sensor is not None:
        logging.info(
            "automatically exclude sensors with more than {:2.2f} % of missing values".format(na_per_sensor * 100))
        missing_ratio = lines.isna().sum() / len(lines)
        sens_miss = lines.columns[missing_ratio > na_per_sensor]
        if len(sens_miss) > 0:
            logging.warning("removed sensors {}".format(
                {"{}: {:4.2f} %".format(k, v) for k, v in
                 (missing_ratio[missing_ratio > na_per_sensor] * 100).to_dict().items()}))
            lines = lines.loc[:, lines.columns[missing_ratio <= na_per_sensor]]
    else:
        logging.warning("all sensors are included since na_per_sensor is set to None")
    if na_per_date is None:
        logging.debug("automatically exclude values when more than 50% of sensors are missing")
        na_per_date = len(lines.columns) // 2
    logging.info("removing sensor data for days with more than {n} missing values".format(n=na_per_date))
    lines.loc[lines.isna().sum(axis=1) > na_per_date, :] = np.NaN
    if method == 'median':
        logging.info("summarizing measures using {m}".format(m=method))
        summarized = lines.median(axis=1)
    else:
        raise NotImplementedError("no other methods than median are implemented at the moment")
    return summarized


def display_year_on_year_avg_pollutant(data: pd.DataFrame, comp_year: int = None, use_st=False):
    curr_year = datetime.datetime.now().year
    curr_avg = get_yearly_avg(data=data, year=curr_year, keep_date=True).reset_index()
    comp_avg = get_yearly_avg(data=data, year=comp_year).reset_index()
    year_on_year = pd.merge(curr_avg, comp_avg, on=['date_comp'], how='inner',
                            suffixes=(str(curr_year), str(comp_year)))
    year_on_year = year_on_year.drop(columns=['date_comp'])
    # year_on_year = reindex_data(df=year_on_year)
    display_plotly_timestamp(lines=year_on_year, use_st=use_st)


def display_correlogram_matrix(data: pd.DataFrame, n_col: int = 2, use_st=False):
    if use_st:
        st.subheader("Correlogram of weather measures on pollutant")
    w_cols = [c for c in data.columns if data[c].dtype == float and c != 'valore']
    n_rows = len(w_cols) // n_col + 1
    plt.figure(figsize=(10, 20))
    for i, weather_col in enumerate(data[w_cols]):
        plt.subplot(n_rows, n_col, i + 1)
        plt.title(weather_col)
        plt.hexbin(data[weather_col], data['valore'], mincnt=1, bins='log', gridsize=50, cmap=plt.get_cmap('Blues'))
    plt.tight_layout()
    if use_st:
        st.pyplot()
    else:
        plt.show()


def pivot_to_multiple_series(data, id_col='idsensore', value_col='valore', dt_col='data', reind_and_interp=False):
    lines = data.pivot_table(index=dt_col, columns=id_col, values=value_col)
    if reind_and_interp:
        all_dt_idx = pd.date_range(lines.index.min(), lines.index.max())
        lines = lines.reindex(all_dt_idx)
    lines['average'] = lines.mean(axis=1)


if __name__ == '__main__':
    print("ok")
