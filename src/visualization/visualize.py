# -*- coding: utf-8 -*-
import datetime
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from bokeh.models import GMapPlot, GMapOptions, DataRange1d

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


def filter_data(dataset: pd.DataFrame, params: dict) -> pd.DataFrame:
    filter_cond = " & ".join({f"{k}=='{v}'" for k, v in params.items() if v is not None})
    return dataset.query(filter_cond) if filter_cond else dataset


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


def display_plotly_timestamp(lines: pd.DataFrame, color_only_average=False, use_st=False):
    fig = go.Figure()
    value_cols = [c for c in lines.columns if c != 'data']
    for i, line_col in enumerate(value_cols):
        if color_only_average:
            line_color = 'rgb(238,57,57)' if line_col == 'average' else 'rgb(170,170,170)'
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
    initial_range = [lines['data'].max() + pd.DateOffset(months=-2), lines['data'].max()]
    fig['layout']['xaxis'].update(range=[d.strftime('%Y-%m-%d') for d in initial_range])
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


def display_year_on_year_avg_pollutant(data: pd.DataFrame, comp_year: int = None, use_st=False):
    curr_year = datetime.datetime.now().year
    curr_avg = get_yearly_avg(data=data, year=curr_year, keep_date=True).reset_index()
    comp_avg = get_yearly_avg(data=data, year=comp_year).reset_index()
    year_on_year = pd.merge(curr_avg, comp_avg, on=['date_comp'], how='inner',
                            suffixes=(str(curr_year), str(comp_year)))
    year_on_year = year_on_year.drop(columns=['date_comp'])
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



if __name__ == '__main__':
    print("ok")
