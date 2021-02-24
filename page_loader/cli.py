import argparse
import os


def prompt_args():
    parser = argparse.ArgumentParser(prog='page-loader',
                                     usage='%(prog)s [options] <url>',
                                     description='download html page',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter  # noqa: E501
                                     )
    parser.add_argument('-o',
                        '--output [dir]',
                        default=os.getcwd(),
                        help="output dir",
                        dest='OUTPUT'
                        )
    parser.add_argument(dest='URL')
    parser._optionals.title = "Options"
    return parser
