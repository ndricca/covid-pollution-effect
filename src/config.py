import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROC_DATA_DIR = os.path.join(DATA_DIR, 'processed')

AQ_COLS = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']
DT_ID_COLS = ['station_name', 'weekofyear', 'wday']