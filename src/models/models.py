import logging
from abc import ABC, abstractmethod
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.config import RANDOM_FOREST_CONFIG, FEAT_WEATHER_COLS, FEAT_DATE_COLS
from src.models.evaluation import compute_time_series_metrics


class TimeSeriesScoringModel(ABC):
    """
    A model capable of scoring its predictions with appropriate metrics.
    """

    @abstractmethod
    def fit(self, x: pd.DataFrame, y: pd.Series):
        """
        Fit model
        :param x: feature matrix
        :param y: target variable
        :return: a copy of this object fitted to given data
        """
        pass

    @abstractmethod
    def predict(self, x: pd.DataFrame):
        """
        Predict with given features
        :param x: feature matrix
        :return: target variable
        """
        pass

    def score(self, x: pd.DataFrame, y: pd.Series):
        """
        Score the models with time series metrics: MAE, MAPE, R2, MSE, RMSE
        :param x: feature matrix
        :param y: target variable
        :return: a dictionary containing the prediction metrics
        """
        prediction = self.predict(x)
        return compute_time_series_metrics(y=y, predicted=prediction)


class WeatherModel(TimeSeriesScoringModel):

    def __init__(self, model_type, features: list = None, bootstrap_features: list = None,
                 bootstrap: bool = False):
        if model_type == 'random_forest':
            self._model = RandomForestRegressor(**RANDOM_FOREST_CONFIG)
        else:
            raise NotImplementedError('specified model is not available')
        self.features = features
        self.bootstrap_features = bootstrap_features
        self.bootstrap = bootstrap

    def _select_features(self, x: pd.DataFrame):
        if self.features is None:
            self.features = ['date_unix'] + FEAT_DATE_COLS + FEAT_WEATHER_COLS
        try:
            new_x = x[self.features].copy()
            return new_x
        except KeyError as e:
            raise RuntimeError(f'Cannot select required features: {str(e)}') from e

    def _bootstrap_features(self, x: pd.DataFrame) -> pd.DataFrame:
        x_btsp = x.reset_index()
        x_btsp.loc[:, self.bootstrap_features] = x_btsp.loc[:, self.bootstrap_features].sample(frac=1,
                                                                                           replace=True).reset_index()
        x_btsp = x_btsp.set_index('data')
        return x_btsp

    def fit(self, x: pd.DataFrame, y: pd.Series):
        x_train = x.copy()
        x_train = self._select_features(x_train).dropna()
        y_train = y[x_train.index].dropna()
        x_train = x_train.loc[y_train.index, :]
        logging.info("Training model")
        self._model.fit(x_train, y_train)
        return self

    def predict(self, x: pd.DataFrame):
        x_test = self._select_features(x).dropna()
        if self.bootstrap:
            x_test = self._bootstrap_features(x_test)
        prediction = pd.Series(self._model.predict(x_test), index=x_test.index)
        return prediction
