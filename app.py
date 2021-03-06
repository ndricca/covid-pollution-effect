import logging
import pandas as pd
import streamlit as st
import warnings

from src.data.arpa.arpa_quality_raw_funcs import ArpaConnect, get_city_sensor_ids
from src.visualization.visualize import display_plotly_timestamp, display_year_on_year_avg_pollutant, \
    dist_values_from_series, reindex_data, summarize_sensors
from src.data.common_funcs import load_dataset, load_normalized_dataset


@st.cache
def get_sensor_registry(arpa):
    sensor_data = get_city_sensor_ids(arpa=arpa, city='Milano')
    return sensor_data


@st.cache
def load_raw_data():
    raw_data = load_dataset()
    return raw_data


@st.cache
def load_norm_data():
    norm_data = load_normalized_dataset()
    return norm_data


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    warnings.filterwarnings('ignore')

    st.title("Covid-19 effect on pollution")
    arpa = ArpaConnect()
    sensor_registry = get_sensor_registry(arpa=arpa)
    raw_data = load_raw_data()
    norm_data = load_norm_data()
    sensor_types = dist_values_from_series(raw_data['nometiposensore'], add_none='exclude')
    selected_type = st.sidebar.selectbox('Filter by sensor type:', sensor_types)
    since_year = st.sidebar.selectbox('See raw data since:', sorted(list(range(2010, 2021)), reverse=True))

    selected_sensors = raw_data.loc[raw_data['nometiposensore'] == selected_type, 'idsensore'].unique().tolist()
    selected_raw_data = raw_data[raw_data['idsensore'].isin(selected_sensors)]
    selected_norm_data = norm_data[norm_data['idsensore'].isin(selected_sensors)]

    if st.checkbox('show sensor registry:', False):
        st.table(sensor_registry.loc[sensor_registry['nometiposensore'] == selected_type])

    if st.checkbox('raw data: show pollutant timeline since ' + str(since_year), False):
        last_year_selected_raw_data = selected_raw_data[selected_raw_data['data'].dt.year >= since_year]
        lines_last_year_selected_raw_data = last_year_selected_raw_data.pivot_table(index='data', columns='idsensore',
                                                                                    values='valore').reset_index()
        lines_last_year_selected_raw_data = reindex_data(df=lines_last_year_selected_raw_data)
        sens_cols = [c for c in selected_sensors if c in lines_last_year_selected_raw_data.columns]
        if len(sens_cols) == 0:
            raise RuntimeError(
                "None of {l} available when data are filtered since year {y}".format(l=sens_cols, y=since_year))
        lines_last_year_selected_raw_data['med'] = summarize_sensors(
            lines=lines_last_year_selected_raw_data.set_index('data'),
            na_per_sensor=0.3).values
        display_plotly_timestamp(lines=lines_last_year_selected_raw_data, color_only_col='med', use_st=True)

    if st.checkbox('raw data: show year on year comparison on 2019', True):
        display_year_on_year_avg_pollutant(data=selected_raw_data, comp_year=2019, use_st=True)

    if st.checkbox('normalized data: show pollutant timeline since ' + str(since_year), False):
        last_year_selected_norm_data = selected_norm_data[selected_norm_data['data'].dt.year >= since_year]
        lines_last_year_selected_norm_data = last_year_selected_norm_data.pivot_table(index='data', columns='idsensore',
                                                                                      values='valore').reset_index()
        lines_last_year_selected_norm_data = reindex_data(df=lines_last_year_selected_norm_data)
        sens_cols = [c for c in selected_sensors if c in lines_last_year_selected_norm_data.columns]
        if len(sens_cols) == 0:
            raise RuntimeError("None of {l} when data are filtered since year {y}".format(l=sens_cols, y=since_year))
        lines_last_year_selected_norm_data['med'] = summarize_sensors(
            lines=lines_last_year_selected_norm_data.set_index('data'),
            na_per_sensor=0.3).values
        display_plotly_timestamp(lines=lines_last_year_selected_norm_data, color_only_col='med', use_st=True)

    if st.checkbox('normalized data: show year on year comparison on 2019', True):
        display_year_on_year_avg_pollutant(data=selected_norm_data, comp_year=2019, use_st=True)
