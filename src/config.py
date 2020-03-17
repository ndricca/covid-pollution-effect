import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROC_DATA_DIR = os.path.join(DATA_DIR, 'processed')

AQ_DATA_DIR = os.path.join(RAW_DATA_DIR, 'air_quality')
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