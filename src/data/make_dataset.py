# -*- coding: utf-8 -*-
import os

import argparse
import logging
import sys

sys.path.append(os.getcwd())

from src.data.air_quality.air_quality_raw_to_proc import load_stations_data, save_stations_data


def main(input_filepath: str = None, output_filepath: str = None):
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    stations_df = load_stations_data(specific_station_file=input_filepath)
    save_stations_data(stations_df=stations_df, specific_file=output_filepath)


def _setup_parser():
    parser = argparse.ArgumentParser(
        description="Runs data processing scripts to turn raw data into cleaned data ready to be analyzed")
    parser.add_argument("--input_filepath", "-i", action="store", type=str, required=False, default=None,
                        help="Specific input single file name")
    parser.add_argument("--output_filepath", "-o", action="store", type=str, required=False, default=None,
                        help="Specific output single file name")
    return parser


def parse_arguments():
    global input_filepath, output_filepath
    parser = _setup_parser()
    args = parser.parse_args()
    input_filepath = args.input_filepath
    output_filepath = args.output_filepath


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    parse_arguments()
    main()
