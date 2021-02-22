#!/usr/bin/env python3

from page_loader import download
from page_loader.cli import prompt_args


def main():
    args = prompt_args().parse_args()

    try:
        print(download(args.URL, args.OUTPUT))
    except ValueError as error:
        print(error)


if __name__ == '__main__':
    main()
