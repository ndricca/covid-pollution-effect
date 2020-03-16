import streamlit as st
import sys
import matplotlib.pyplot as plt
import logging

from src.data.air_quality.air_quality_proc import load_proc_data, year_on_year_comparison, plot_year_on_year_comparison
from src.config import AQ_COLS


@st.cache
def load_data():
    data = load_proc_data()
    return data

@st.cache
def filter_data(data, station, curr_year, comp_year):
    stat_data = data.loc[data['station_name'] == station, :]
    yoy_df = year_on_year_comparison(dt_stations_df=data, curr_year=curr_year, comp_year=comp_year)
    return yoy_df


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    st.title("Covid-19 effect on Milan pollution")

    data = load_data()
    station = st.selectbox("Station name:", data['station_name'].unique())
    curr_yr_ls = sorted(data['year'].unique(),reverse=True)
    curr_year = st.selectbox("Current year:", curr_yr_ls)
    comp_yr_ls = [y for y in curr_yr_ls if y != curr_year]
    comp_year = st.selectbox("Comparison year:", comp_yr_ls)
    filtered = filter_data(data=data, station=station, curr_year=curr_year, comp_year=comp_year)
    if st.checkbox("Show data", False):
        st.write(filtered)
    aq_col = st.selectbox("Air pollutant:", AQ_COLS)
    st.line_chart(plot_year_on_year_comparison(filtered, aq_col=aq_col))