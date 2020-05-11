import logging
import os
import pandas as pd
from sodapy import Socrata
from pathlib import Path
from dotenv import load_dotenv

from src.config import PROJECT_DIR, ARPA_DATA_DIR, ARPA_REG_DATA_ID, ARPA_MEASURES_DATA_ID, PROC_DATA_DIR, ARPA_STATIONS


class ArpaConnect:
    """
    Simple connector to Socrata API used to get current ARPA air quality open data.
    Connection parameters are written into .env private file.
    """

    def __init__(self):
        self.params_dict = {}
        self._init_connection()

    def _init_connection(self):
        load_dotenv(Path(PROJECT_DIR) / '.env')
        logging.info("Connecting with Socrata backend for recent data")
        self.params_dict = {
            'domain': os.environ.get('ARPA_WEB_DOMAIN'),
            'app_token': os.environ.get('ARPA_APP_TOKEN'),
            'username': os.environ.get('ARPA_USER_NAME'),
            'password': os.environ.get('ARPA_PWD')
        }
        self.connector = Socrata(**self.params_dict)
        logging.info("Backend connected")

    def get_df(self, dataset_identifier, **kwargs):
        logging.info("Download from Socrata dataset {d} {kw}".format(d=dataset_identifier,
                                                                     kw="with kwargs " + str(kwargs) if len(
                                                                         kwargs) > 0 else ""))
        results = self.connector.get(dataset_identifier, **kwargs)
        results_df = pd.DataFrame.from_records(results)
        return results_df


def get_city_sensor_ids(arpa: ArpaConnect, city: str=None, prov: str=None) -> pd.DataFrame:
    """Get dataframe with sensor id, type and location """
    where_component = ["datastop IS NULL"]
    if city is not None:
        city_cond = 'comune = "{}"'.format(city)
        where_component.append(city_cond)
    if prov is not None:
        prov_cond = 'provincia = "{}"'.format(prov)
        where_component.append(prov_cond)
    where_cond = " and ".join(where_component)
    reg_df = arpa.get_df(ARPA_REG_DATA_ID,
                         where=where_cond,
                         order="idsensore")
    return reg_df


def get_current_sensor_data(arpa: ArpaConnect, id_data: pd.DataFrame, dataset_identifier: str = None) -> pd.DataFrame:
    """ Get dataframe with all sensor data for selected sensor id dataframe. """
    if dataset_identifier is None:
        dataset_identifier = ARPA_MEASURES_DATA_ID
    where = "idsensore IN (" + str(id_data['idsensore'].to_list())[1:-1] + ")"
    sensor_df = arpa.get_df(dataset_identifier=dataset_identifier, where=where, limit=6000000)
    return sensor_df


def get_historical_sensor_data(id_data: pd.DataFrame) -> pd.DataFrame:
    """ Load all data from previous years for selected sensor id dataframe. """
    files = [file for file in os.listdir(ARPA_DATA_DIR) if file.endswith('.zip')]
    hist_list = []
    csv_kwargs = {
        'compression': 'zip',
        'parse_dates': ['Data'],
        'dtype': {'IdSensore': str, 'valore': float}
    }
    id_data = id_data.loc[:, ["idsensore", "nometiposensore", "idstazione"]]
    for f in files:
        logging.info("Loading sensor data {}".format(f))
        hist_single_df = pd.read_csv(os.path.join(ARPA_DATA_DIR, f), **csv_kwargs)
        hist_single_df.columns = [c.lower() for c in hist_single_df.columns]
        merged_single_df = pd.merge(hist_single_df, id_data, on='idsensore', how='inner')
        merged_single_df = merged_single_df.loc[merged_single_df['valore'] != -9999]
        merged_single_df = merged_single_df.drop(columns=['idoperatore'])
        hist_list.append(merged_single_df)
    hist_df = pd.concat(hist_list)
    return hist_df


def load_historical_data(id_data: pd.DataFrame, build_historical: bool = False) -> pd.DataFrame:
    if build_historical:
        logging.info("Create historical arpa dataframe from zipped csv")
        hist_df = get_historical_sensor_data(id_data=id_data)
    else:
        input_path = os.path.join(ARPA_DATA_DIR, 'history_df.pkl')
        logging.info("Create historical arpa dataframe from builded pickle")
        hist_df = pd.read_pickle(input_path)
    return hist_df


def clean_current_sensor_df(sensor_df: pd.DataFrame, id_data: pd.DataFrame) -> pd.DataFrame:
    """ Handle NA values, columns type, merge id info. """
    cleaned_sensor_df = sensor_df.loc[sensor_df['valore'] != '-9999']
    cleaned_sensor_df['valore'] = cleaned_sensor_df['valore'].astype(float)
    cleaned_sensor_df['data'] = pd.to_datetime(cleaned_sensor_df.data)
    cleaned_sensor_df = cleaned_sensor_df.drop(columns='idoperatore')
    id_data = id_data.loc[:, ["idsensore", "nometiposensore", "idstazione"]]
    merged_sensor_df = pd.merge(cleaned_sensor_df, id_data, on=['idsensore'])
    return merged_sensor_df


def get_all_sensor_data(arpa: ArpaConnect, station: str = None, build_historical: bool = False) -> pd.DataFrame:
    id_data = get_city_sensor_ids(arpa=arpa, city=station)
    current_sensor_df = get_current_sensor_data(arpa=arpa, id_data=id_data)
    if len(current_sensor_df) == 0:
        raise RuntimeError("no current data available for selected sensors")
    current_df = clean_current_sensor_df(sensor_df=current_sensor_df, id_data=id_data)
    historical_cleaned_df = load_historical_data(id_data=id_data, build_historical=build_historical)
    all_sensor_df = pd.concat([historical_cleaned_df, current_df])
    return all_sensor_df


def save_all_sensor_data(all_sensor_df, specific_file: str = None):
    if specific_file is None:
        specific_file = 'arpa_data.pkl'
    path_to_output = os.path.join(PROC_DATA_DIR, specific_file)
    logging.info("saving arpa dataframe as pickle in {f}".format(f=specific_file))
    all_sensor_df.to_pickle(path_to_output)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    arpa = ArpaConnect()
    logging.info("building ARPA {}".format("history_df.pkl"))
    hist_arpa_list = []
    for station in ARPA_STATIONS:
        id_data = get_city_sensor_ids(arpa=arpa, city=station)
        stat_hist_arpa_df = get_historical_sensor_data(id_data=id_data)
        hist_arpa_list.append(stat_hist_arpa_df)
    hist_arpa_df = pd.concat(hist_arpa_list)
    out_hist_path = os.path.join(ARPA_DATA_DIR, 'history_df.pkl')
    logging.info("saving to {}".format(out_hist_path))
    hist_arpa_df.to_pickle(out_hist_path)
