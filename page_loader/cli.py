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
                        dest='output'
                        )
    parser.add_argument('-t',
                        '--threads [number]',
                        default=1,
                        help="threads number",
                        dest='threads',
                        type=int
                        )
    parser.add_argument('--verbose',
                        '-v',
                        action='count',
                        dest='verbosity',
                        default=0,
                        help="verbosity level"
                        )
    parser.add_argument(dest='url')
    parser._optionals.title = "Options"
    return parser
