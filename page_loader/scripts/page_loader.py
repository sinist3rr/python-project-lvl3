#!/usr/bin/env python3

import logging.config
import sys
from page_loader.logger_config import generate_logger_config
from page_loader import download
from page_loader.cli import prompt_args


def main():
    log_levels = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    args = prompt_args().parse_args()
    logging.config.dictConfig(generate_logger_config(log_levels[args.verbosity]))  # noqa: E501

    try:
        print(download(args.url, args.output))
        sys.exit(0)
    except ValueError as error:
        print(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
