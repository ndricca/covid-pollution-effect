# -*- coding: utf-8 -*-
import os

import click
import logging
from dotenv import find_dotenv, load_dotenv
import sys

from src.data.air_quality.air_quality_data import load_stations_data, save_stations_data


@click.command()
@click.argument('input_filepath', type=click.Path())
@click.argument('output_filepath', type=click.Path())
def main(input_filepath: str = None, output_filepath: str = None):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    stations_df = load_stations_data(specific_station_file=input_filepath)
    save_stations_data(stations_df=stations_df, specific_file=output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
