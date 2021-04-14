#!/usr/bin/env python3

import logging.config
import sys
from page_loader.logger_config import generate_logger_config
from page_loader import download
from page_loader.cli import prompt_args
from page_loader.errors import AppInternalError


def main():
    log_levels = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    args = prompt_args().parse_args()
    logging.config.dictConfig(
        generate_logger_config(log_levels[args.verbosity])
    )

    try:
        print(download(args.url, args.output))
        sys.exit(0)
    except AppInternalError:
        sys.exit(1)


if __name__ == '__main__':
    main()
