import datetime
import logging
import streamlit as st

from src.models.train_model import normalize_from_data
from src.visualization.visualize import dataset_for_viz, create_params_dict, create_select_box, filter_data, \
    display_correlogram_matrix, filter_dates, display_sensor_scatter, display_plotly_timestamp, \
    display_year_on_year_avg_pollutant


@st.cache
def load():
    data = dataset_for_viz()
    return data


@st.cache
def filter_with_params(data, params):
    vega = filter_data(dataset=data, params=params)
    return vega


def normalize(data, params_dict=None, start_date=None):
    if params_dict is not None:
        data = filter_with_params(data=data, params=params_dict)
    if start_date is not None:
        data = filter_dates(dataset=data, start_date=start_date)
    norm_data = normalize_from_data(dataset=data)
    return norm_data


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    st.title("Covid-19 effect on pollution")
    data = load()
    params_dict = create_params_dict(dataset=data)
    place_holders = {k: st.empty() for k in params_dict.keys()}
    boxes = create_select_box(st=st.sidebar, params_dict=params_dict, ph=place_holders)
    vega = filter_with_params(data, boxes)

    if st.checkbox('show sensor registry:', False):
        st.table(vega.loc[:, ['idsensore', 'nometiposensore', 'idstazione']].drop_duplicates().reset_index())

    if st.checkbox('filter dates:', False):
        start_date = st.date_input('start date:', datetime.date(2019, 1, 1))
        vega = filter_dates(dataset=vega, start_date=start_date)
    else:
        start_date = None

    if st.checkbox('show pollutant timeline', False):
        lines = vega.pivot_table(index='data', columns='idsensore', values='valore').reset_index()
        display_plotly_timestamp(lines=lines)

    if st.checkbox('show year on year comparison', True):
        year_list = [y for y in vega['data'].dt.year.unique() if y != datetime.datetime.now().year]
        year = st.selectbox('compare year:', sorted(year_list, reverse=True))
        st.subheader('raw comparison')
        display_year_on_year_avg_pollutant(data=vega, comp_year=year)
        st.subheader('normalized comparison')
        norm_data = normalize(data=data, start_date=start_date, params_dict=boxes)
        display_year_on_year_avg_pollutant(data=norm_data, comp_year=year)

    if st.checkbox('show selected weather impact on pollutant per sensor', False):
        weather_infos = list(set(['umidita_perc'] + sorted([c for c in vega.columns if len(c.split("_")) > 1])))
        weather_info = st.selectbox("weather info: ", weather_infos)
        display_sensor_scatter(data=vega, weather_info=weather_info)

    if st.checkbox('show all weather impact on pollutant', False):
        display_correlogram_matrix(data=vega)
