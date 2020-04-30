import os
import sys
import pandas as pd
from tqdm import tqdm
import logging

from src.config import BOOTSTRAP_SAMPLES, FEAT_WEATHER_COLS, FEAT_CAL_COLS, PROC_DATA_DIR
from src.data.common_funcs import load_dataset
from src.features.build_features import build_dataset_features, filter_by_sensor
from src.models.models import WeatherModel


def x_y_train_test_split(dataset: pd.DataFrame, year_test: int = None, y_col: str = 'valore') -> tuple:
    y = dataset[y_col]
    x = dataset.drop(columns=[y_col])
    x_train = x.copy().iloc[x.index.year <= year_test]
    x_test = x.copy().iloc[x.index.year == year_test]
    y_train = y.copy()[y.index.year <= year_test]
    y_test = y.copy()[y.index.year == year_test]
    return x_train, x_test, y_train, y_test


def x_y_split(dataset: pd.DataFrame, y_col: str = 'valore') -> tuple:
    y = dataset[y_col]
    x = dataset.drop(columns=[y_col])
    return x, y


def train_test_pipeline():
    dataset = load_dataset()
    sensor_dummies = True if len(sys.argv) > 1 and sys.argv[1] == '-all' else False
    if not sensor_dummies:
        dataset = filter_by_sensor(dataset=dataset, filter_dict={})
    dataset_with_features = build_dataset_features(dataset=dataset, sensor_dummies=sensor_dummies)
    x_train, x_test, y_train, y_test = x_y_train_test_split(dataset=dataset_with_features, year_test=2019)
    model = WeatherModel(model_type='random_forest')
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    compare_df = pd.merge(pd.DataFrame({'test': y_test}), pd.DataFrame({'pred': y_pred}), left_index=True,
                          right_index=True, how='left')
    return compare_df


def bootstrap_normalization(model, x):
    result_df = pd.DataFrame()
    for i in tqdm(range(BOOTSTRAP_SAMPLES + 1)):
        result_df["sim_" + str(i)] = model.predict(x)
    normalized_df = result_df.mean(axis=1)
    normalized_df = normalized_df.reset_index()
    normalized_df.columns = ['data', 'valore']
    return normalized_df


def normalize_from_data(dataset: pd.DataFrame):
    dataset_with_features = build_dataset_features(dataset=dataset,sensor_dummies=False)
    x, y = x_y_split(dataset=dataset_with_features)
    features = ['date_unix'] + FEAT_CAL_COLS + FEAT_WEATHER_COLS
    bootstrap_features = [f for f in features if f != 'date_unix']
    norm_model = WeatherModel(model_type='random_forest',
                              features=features,
                              bootstrap_features=bootstrap_features,
                              bootstrap=True)
    norm_model.fit(x, y)
    normalized = bootstrap_normalization(model=norm_model, x=x)
    return normalized


def normalize_pollutant_pipeline(filter_dict: dict, sensor_dummies: bool = None):
    dataset = load_dataset()
    if sensor_dummies is None:
        sensor_dummies = False
    if not sensor_dummies:
        dataset = filter_by_sensor(dataset=dataset, filter_dict=filter_dict)
    normalized = normalize_from_data(dataset, sensor_dummies)
    return normalized


def pipeline_normalize_multi_sensors(sensors_list: list = None):
    dataset = load_dataset()
    if sensors_list is None:
        sensors_list = dataset['idsensore'].unique().tolist()
    sensors_dataset = dataset.loc[dataset['idsensore'].isin(sensors_list)]
    normalized_dataset = pd.DataFrame()
    for sensor in tqdm(sensors_list):
        sensor_dataset = sensors_dataset.loc[sensors_dataset['idsensore']==sensor]
        logging.info("normalizing data for sensor " + sensor)
        norm_sensor = normalize_from_data(dataset=sensor_dataset)
        norm_sensor['idsensore'] = sensor
        normalized_dataset = pd.concat([normalized_dataset, norm_sensor])
    output_pkl = os.path.join(PROC_DATA_DIR, 'normalized_dataset.pkl')
    normalized_dataset.to_pickle(output_pkl)


if __name__ == '__main__':
    sensor_dummies = True if len(sys.argv) > 1 and sys.argv[1] == '-all' else False
    filter_dict = {}
    normalized_df = normalize_pollutant_pipeline(filter_dict=filter_dict, sensor_dummies=sensor_dummies)
    normalized_df.plot()
