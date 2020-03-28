import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROC_DATA_DIR = os.path.join(DATA_DIR, 'processed')

AQ_DATA_DIR = os.path.join(RAW_DATA_DIR, 'aqicn')
WT_DATA_DIR = os.path.join(RAW_DATA_DIR, 'weather')
ARPA_DATA_DIR = os.path.join(RAW_DATA_DIR, 'arpa_quality')

AQ_COLS = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']
DT_ID_COLS = ['station_name', 'month', 'day']
# DT_ID_COLS = ['station_name', 'weekofyear', 'wday']

WT_STATIONS = ['Milano']
WT_BASE_URL = "https://www.ilmeteo.it/portale/archivio-meteo/"
WT_START_YEAR = '2005'
ITA_MONTHS = {
    "01": "Gennaio",
    "02": "Febbraio",
    "03": "Marzo",
    "04": "Aprile",
    "05": "Maggio",
    "06": "Giugno",
    "07": "Luglio",
    "08": "Agosto",
    "09": "Settembre",
    "10": "Ottobre",
    "11": "Novembre",
    "12": "Dicembre",
}

ARPA_REG_DATA_ID = 'ib47-atvt'
ARPA_MEASURES_DATA_ID = 'nicp-bhqi'
ARPA_MEASURES_FREQ = {
    'hourly': ['Ossidi di Azoto', 'Biossido di Azoto', 'Biossido di Zolfo', 'Ozono',
               'Ammoniaca', 'Monossido di Carbonio', 'Benzene', 'Benzo(a)pirene',
               'Nikel', 'Arsenico', 'Cadmio', 'Piombo', 'BlackCarbon'],
    'daily': ['PM10 (SM2005)', 'Particelle sospese PM2.5']
}

DEFAULT_PLOTLY_COLORS = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                         'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                         'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                         'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                         'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

DEFAULT_PLOTLY_XAXIS_CFG = {
    'rangeselector': {'buttons': list([
        {'count': 1, 'label': "1m", 'step': "month", 'stepmode': "backward"},
        {'count': 6, 'label': "6m", 'step': "month", 'stepmode': "backward"},
        {'count': 1, 'label': "YTD", 'step': "year", 'stepmode': "todate"},
        {'count': 1, 'label': "1y", 'step': "year", 'stepmode': "backward"},
        {'step': "all"}
    ])},
    'rangeslider': {'visible': True},
    'type': "date"
}

FEAT_KEEP_DTYPES = ['float', 'int32', 'int64', 'uint8']
FEAT_WEATHER_COLS = ['tmedia_celsius', 'tmin_celsius', 'tmax_celsius', 'puntorugiada_celsius',
                     'umidita_perc', 'visibilita_km', 'ventomedia_kmh', 'ventomax_kmh', 'raffica_kmh',
                     'pressioneslm_mb', 'pressionemedia_mb', 'pioggia_mm']
FEAT_WEATHER_EVENTS_COLS = ['grandine', 'temporale', 'neve', 'pioggia', 'nebbia']
FEAT_CAL_COLS = ['year', 'day', 'weekofyear', 'dayofyear']
FEAT_MONTH_COLS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
FEAT_WEEK_COLS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
FEAT_DATE_COLS = FEAT_CAL_COLS + FEAT_MONTH_COLS + FEAT_WEEK_COLS

RANDOM_FOREST_CONFIG = {
    'n_estimators': 20
}
BOOTSTRAP_SAMPLES = 100

FOLIUM_CFG = {
    'location': [45.4646602, 9.1889546],
    'tiles': 'Stamen Toner',
    'zoom_start': 12
}
