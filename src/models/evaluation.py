import numpy as np
import pandas as pd
from sklearn import metrics


def mean_absolute_percentage_error(y, predicted):
    """
    Compute mean absolute percentage error (MAPE) between y and prediction
    :param y: actual target variable
    :param predicted: predicted target variable
    :return: the scalar mape
    """
    return np.mean(np.abs((y - predicted) / y))


def predict_ann(model, x_test):
    """
    Compute prediction from a keras ann model
    :param model: a trained keras model
    :param x_test: matrix of test features
    :return: model prediction
    """
    ann_y_hat = model.predict(x_test)
    ann_y_hat = np.array([item for sublist in ann_y_hat for item in sublist])
    return ann_y_hat


def compute_time_series_metrics(y, predicted):
    """
    Compute a bunch of useful error metrics for time series, including mape, mae and rmse
    :param y: actual target variable
    :param predicted: predicted target variable
    :return: a dictionary of metrics and their values
    """
    err = y - predicted
    rel_err = err / y
    res = {
        'mae': metrics.mean_absolute_error(y, predicted),
        'mape': mean_absolute_percentage_error(y, predicted),
        'mse': metrics.mean_squared_error(y, predicted),
        'rmse': np.sqrt(metrics.mean_squared_error(y, predicted)),
        'r2': metrics.r2_score(y, predicted),
        'bias': np.mean(err),
        'sd': np.std(err),
        'corr': np.corrcoef(y, predicted)[0][1],
        'mad': np.median(np.abs(err)) - np.median(err),
        'max_ae': np.max(np.abs(err)),
        'max_mape': np.max(np.abs(rel_err))
    }
    return res


def compute_metrics_dataframe(y, predicted, model_name, existing_metrics=pd.DataFrame(), scaler=None, scale_y=False,
                              scale_predicted=False):
    """
    Compute time series metrics and return them as a pandas dataframe
    :param y: actual target variable
    :param predicted: predicted target variable
    :param model_name: name of the tested model
    :param existing_metrics: pandas dataframe of metrics to be concatenated to the new one
    :param scaler: a sklearn scaler to be used on y or predicted
    :param scale_y: shall y variable be inverse transformed
    :param scale_predicted: shall prediction be inverse transformed
    :return: a pandas dataframe with error metrics
    """
    if scale_y:
        y = scaler.inverse_transform(np.array(y).reshape(-1, 1))
    if scale_predicted:
        predicted = scaler.inverse_transform(np.array(predicted).reshape(-1, 1))

    existing = existing_metrics.copy()
    res = pd.DataFrame(compute_time_series_metrics(y, predicted), index=[model_name])
    res = pd.concat([existing, res])
    res = res[~res.index.duplicated(keep='last')]
    res.sort_values(by='mape', inplace=True)
    return res

