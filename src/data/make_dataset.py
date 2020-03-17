# -*- coding: utf-8 -*-
import os
import logging
import sys

sys.path.append(os.getcwd())


def main():
    logging.info('making final data set from raw data')
    pass


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
