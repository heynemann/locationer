#!/usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing

from derpconf.config import Config, generate_config

Config.define('COOKIE_SECRET', '161740d090204f2182bdd0ac47cddd0f', 'To sign secure cookie info.', 'Basic')

Config.define('REDIS_HOST', '127.0.0.1', 'The host where the Redis server is running.', 'Cache')
Config.define('REDIS_PORT', 7775, 'The port that Redis server is running.', 'Cache')
Config.define('REDIS_DB_COUNT', 0, 'The number of redis db.', 'Cache')
Config.define('REDIS_PASSWORD', '', 'The redis password', 'Cache')

Config.define('NUMBER_OF_FORKS', multiprocessing.cpu_count(), 'Number of forks to use for tornado process. Defaults to number of cpus.', 'Runtime')

Config.define('STATIC_URL', '/static/', 'Static files route.', 'Static')


if __name__ == '__main__':
    generate_config()
