import logging
import sys
import pandas as pd

from src.config import FEAT_KEEP_DTYPES
from src.data.common_funcs import load_dataset
from src.features.seasonality_features import add_harmonics
from src.features.weather_features import create_weather_events


def build_dataset_with_sensor_dummies(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset_with_dummies = pd.get_dummies(dataset, columns=['idsensore', 'nometiposensore', 'idstazione'],
                                          prefix_sep='_')
    return dataset_with_dummies


def build_calendar_features(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset_with_calendar = dataset.copy()
    dataset_with_calendar['year'] = dataset_with_calendar['data'].dt.year
    dataset_with_calendar['month_name'] = dataset_with_calendar['data'].dt.month_name()
    dataset_with_calendar['day'] = dataset_with_calendar['data'].dt.day
    dataset_with_calendar['day_of_week'] = dataset_with_calendar['data'].dt.strftime('%A')
    dataset_with_calendar['weekofyear'] = dataset_with_calendar['data'].dt.weekofyear
    dataset_with_calendar['dayofyear'] = dataset_with_calendar['data'].dt.dayofyear
    dataset_with_calendar['date_unix'] = dataset_with_calendar['data'].astype('int64') / 1e09
    dataset_with_calendar = pd.get_dummies(dataset_with_calendar, columns=['day_of_week', 'month_name'], prefix='',
                                           prefix_sep='')
    return dataset_with_calendar


def build_date_features(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset_with_calendar = build_calendar_features(dataset=dataset)
    dataset_with_harmonics = add_harmonics(dataset=dataset_with_calendar.set_index('data'),
                                           periods=[(7, 3), (365.24, 3)]).reset_index()
    return dataset_with_harmonics


def select_numerical_columns(dataset: pd.DataFrame, dtypes_to_include: list = None) -> pd.DataFrame:
    if dtypes_to_include is None:
        dtypes_to_include = FEAT_KEEP_DTYPES
    return dataset.select_dtypes(include=dtypes_to_include)


def build_dataset_features(dataset: pd.DataFrame, sensor_dummies: bool) -> pd.DataFrame:
    if sensor_dummies:
        dataset = build_dataset_with_sensor_dummies(dataset=dataset)
    dataset_with_weather_events = create_weather_events(weather_df=dataset)
    dataset_with_date_features = build_date_features(dataset=dataset_with_weather_events)
    dataset_with_date_index = dataset_with_date_features.set_index('data')
    dataset_with_int_cols = select_numerical_columns(dataset=dataset_with_date_index)
    return dataset_with_int_cols


if __name__ == '__main__':
    dataset = load_dataset()
    sensor_dummies = True if len(sys.argv) > 1 and sys.argv[1] == '-all' else False
    dataset_with_features = build_dataset_features(dataset=dataset, sensor_dummies=sensor_dummies)
