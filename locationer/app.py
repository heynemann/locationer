#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import abspath, join, dirname

import _mysql
import tornado.web
from tornado.web import url

from locationer.handlers import HomeHandler, LocationsHandler


def configure_app(self, config=None, log_level='INFO', debug=False, static_path=None):
    template_path = abspath(join(dirname(__file__), 'templates'))
    static_path = abspath(join(dirname(__file__), 'static'))

    self.config = config

    handlers = [
        url(r'/', HomeHandler, name="home"),
        url(r'/locations', LocationsHandler, name="location"),
    ]

    self.db = _mysql.connect(
        host="localhost", user="root",
        passwd="", db="locationer")

    options = {
        "cookie_secret": self.config.COOKIE_SECRET,
        "template_path": template_path,
        "static_path": static_path,
        "static_url_prefix": self.config.STATIC_URL
    }

    if debug:
        options['debug'] = True

    return handlers, options


class LocationApp(tornado.web.Application):

    def __init__(self, config=None, log_level='INFO', debug=False, static_path=None):
        handlers, options = configure_app(self, config, log_level, debug, static_path)
        super(LocationApp, self).__init__(handlers, **options)
