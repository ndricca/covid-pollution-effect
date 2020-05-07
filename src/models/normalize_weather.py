# -*- coding: utf-8 -*-
import os
import logging
import sys
import warnings

sys.path.append(os.getcwd())
warnings.filterwarnings('ignore')

from src.models.train_model import pipeline_normalize_multi_sensors


def predict_normalized_pollutant():
    """
    Build total dataset merging ARPA air quality data with weather data.
    """
    logging.info('normalize all sensors available into dataset')
    pipeline_normalize_multi_sensors()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    predict_normalized_pollutant()
