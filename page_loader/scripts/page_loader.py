#!/usr/bin/env python3

import logging.config
from page_loader.logger_config import generate_logger_config
from page_loader import download
from page_loader.cli import prompt_args


def main():
    log_levels = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARN,
        3: logging.INFO,
        4: logging.DEBUG,
    }

    args = prompt_args().parse_args()
    logging.config.dictConfig(generate_logger_config(log_levels[args.verbosity]))  # noqa: E501

    try:
        print(download(args.url, args.output))
    except ValueError as error:
        print(error)


if __name__ == '__main__':
    main()
