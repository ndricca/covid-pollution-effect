from datetime import datetime, date

import numpy as np
import pandas as pd


def harmonics(dates, period, n, epoch=datetime(1900, 1, 1)):
    """
    Computes harmonics for the given dates. Each harmonic is made of a couple of sinusoidal and cosinusoidal waves
    with frequency i/period, i = 1...n. The argument of the functions is the number of hour from epoch.
    :param dates: a pandas series pf dates
    :param period: the base period of the harmonics
    :param n: the number of harmonics to include
    :param epoch: the epoch used to compute the argument of the sin
    :return: a pandas dataframe with dates as index and harmonics as columns
    """
    d = pd.DataFrame(index=dates)
    hours = (dates - epoch) / pd.Timedelta(hours=1)

    for i in range(1, n + 1):
        d[f'Sin_{round(period)}_{i}'] = np.sin(2 * i * np.pi * hours / period)
        d[f'Cos_{round(period)}_{i}'] = np.cos(2 * i * np.pi * hours / period)

    return d


def _add_harmonics(df: pd.DataFrame, period, n):
    harm = harmonics(df.index, period, n)
    return pd.concat([df, harm], axis=1)


def add_harmonics(dataset: pd.DataFrame, periods):
    """
    Add to dataset harmonics as specified by periods. Parameter periods shall be a list-like object of integer-valued
    tuples (period, number_of_harmonics), where period is the period of the sinusoidal waves while number_of_harmonics
    is the number of harmonics to include. Each of the i harmonics, i = 1...number_of_harmonics
    is a couple of sinusoidal waves with frequency i/period [hours].
    :param dataset: a pandas dataframe with a datetime index
    :param periods: list-like object of integer-valued tuples (period, number_of_harmonics)
    :return: the given dataframe with harmonics as additional columns
    """
    d = dataset.copy()

    for period, n in periods:
        d = _add_harmonics(d, period, n)

    return d

