#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from os.path import abspath, join, dirname, isabs, expanduser, split
import os

import tornado.ioloop
from tornado.httpserver import HTTPServer

from locationer.app import LocationApp
from locationer.config import Config

LOGS = {
    0: 'error',
    1: 'warning',
    2: 'info',
    3: 'debug'
}

ROOT_PATH = abspath(join(dirname(__file__), '..'))
DEFAULT_CONFIG_PATH = join(ROOT_PATH, 'config', 'local.conf')


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default="3000", help="Port to start the server with.")
    parser.add_argument('--bind', '-b', default="0.0.0.0", help="IP to bind the server to.")
    parser.add_argument('--conf', '-c', default=DEFAULT_CONFIG_PATH, help="Path to configuration file.")
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Log level: v=warning, vv=info, vvv=debug.')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Indicates whether to run tornado in debug mode.')

    options = parser.parse_args(args)

    log_level = LOGS[options.verbose].upper()
    logging.basicConfig(level=getattr(logging, log_level), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if not isabs(options.conf):
        logging.debug("Configuration file {0} is not absolute. Converting to abspath".format(options.conf))
        options.conf = abspath(options.conf)

    logging.info("Loading configuration file at {0}...".format(options.conf))

    config = Config.load(path=options.conf, conf_name=split(options.conf)[-1], lookup_paths=[
        os.curdir,
        expanduser('~'),
        '/etc/',
    ])

    logging.info("Using configuration file at {0}.".format(config.config_file))

    application = LocationApp(config, log_level, options.debug)
    server = HTTPServer(application, xheaders=True)

    server.bind(options.port, options.bind)
    server.start(1)

    logging.info('-- Locationer started listening in %s:%d --' % (options.bind, options.port))
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.info('')
        logging.info('-- Locationer closed by user interruption --')

if __name__ == '__main__':
    main(sys.argv[1:])
