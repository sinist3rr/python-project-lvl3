import argparse


def prompt_args():
    parser = argparse.ArgumentParser(prog='page-loader',
                                     usage='%(prog)s [options] <url>',
                                     description='download html page')
    parser.add_argument('-o', '--output [dir]',
                        dest='OUTPUT', default='/app',
                        help="output dir")
    parser.add_argument(dest='URL')
    parser._optionals.title = "Options"
    return parser
