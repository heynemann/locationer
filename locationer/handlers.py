#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import tornado.web
from json import dumps


logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    def render(self, template_name, *args, **kwargs):
        logger.debug('rendering template {}'.format(template_name))

        kwargs['handler'] = self
        return super(BaseHandler, self).render(template_name, *args, **kwargs)

    @property
    def config(self):
        return self.application.config

    @property
    def redis(self):
        return self.application.redis


class HomeHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        context = {}
        self.render('index.html', **context)


class LocationsHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        zipcode = self.get_argument('zipcode')

        items = tuple(self.redis.smembers(zipcode.upper()))

        self.write(dumps(items))
        self.finish()
