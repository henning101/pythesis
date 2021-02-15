import os
import argparse

args = None
argparser = argparse.ArgumentParser(description='PyThesis - A LaTeX Framework')

def parse_args():
    """ Parses user arguments.
    """
    global args
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--host',
        action='store',
        dest='host',
        help='Server host',
        default='0.0.0.0'
    )
    argparser.add_argument(
        '--port',
        action='store',
        dest='port',
        help='Server port',
        type=int,
        default=5000
    )
    argparser.add_argument(
        '--project_root',
        action='store',
        dest='project_root',
        help='Project root',
        required=True
    )
    argparser.add_argument(
        '--main_document',
        action='store',
        dest='main_document',
        help='Main document (enter without a file extension)',
        default='document'
    )
    argparser.add_argument(
        '--matlab',
        action='store_true',
        dest='matlab',
        help='Create a MATLAB session'
    )
    argparser.add_argument(
        '-l',
        '--loglevel',
        action='store',
        dest='loglevel',
        help='set log level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info'
    )
    argparser.add_argument(
        '--logger',
        action='store',
        dest='logger',
        help='sets a logger',
        default=''
    )
    argparser.add_argument(
        '--debug',
        action='store_true',
        dest='debug',
        help='Enables debug mode (avoids Flask reloads)',
    )
    argparser.add_argument(
        '--build_config',
        action='store',
        dest='build_config',
        help='LaTeX build config path',
        default='./build.config'
    )
    args = argparser.parse_args()
