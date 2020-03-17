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
    yoy_df = year_on_year_comparison(dt_stations_df=stat_data, curr_year=curr_year, comp_year=comp_year)
    return yoy_df


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    st.title("Covid-19 effect on pollution")

    data = load_data()
    station = st.sidebar.selectbox("Station name:", data['station_name'].unique())
    curr_yr_ls = sorted(data['year'].unique(), reverse=True)
    curr_year = st.sidebar.selectbox("Current year:", curr_yr_ls)
    comp_yr_ls = [y for y in curr_yr_ls if y != curr_year]
    comp_year = st.sidebar.selectbox("Comparison year:", comp_yr_ls)
    filtered = filter_data(data=data, station=station, curr_year=curr_year, comp_year=comp_year)
    if st.checkbox("Show data", False):
        st.write(filtered[[c for c in filtered.columns if c.split("_")[0] in AQ_COLS]])
    aq_col = st.sidebar.selectbox("Air pollutant:", AQ_COLS)
    smooth = st.sidebar.checkbox("Smooth", False)
    st.subheader("Timeline for station {s}".format(s=station))
    st.line_chart(
        plot_year_on_year_comparison(filter_data(data=data, station=station, curr_year=curr_year, comp_year=comp_year),
                                     aq_col=aq_col, smooth=smooth))