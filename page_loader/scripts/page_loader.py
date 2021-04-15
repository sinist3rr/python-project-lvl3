#!/usr/bin/env python3

import logging.config
import sys
import page_loader.logger_config
import page_loader.cli
from page_loader import download
from page_loader.errors import AppInternalError


def main():
    log_levels = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    args = page_loader.cli.prompt_args().parse_args()
    logging.config.dictConfig(
        page_loader.logger_config.generate(log_levels.get(args.verbosity))
    )

    try:
        print(download(args.url, args.output))
        sys.exit(0)
    except AppInternalError:
        sys.exit(1)


if __name__ == '__main__':
    main()
