#!/usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing

from derpconf.config import Config, generate_config

Config.define('COOKIE_SECRET', '161740d090204f2182bdd0ac47cddd0f', 'To sign secure cookie info.', 'Basic')

Config.define('MYSQL_HOST', '127.0.0.1', 'The host where the MYSQL server is running.', 'Database')
Config.define('MYSQL_PORT', 7775, 'The port that MYSQL server is running.', 'Database')
Config.define('MYSQL_DATABASE', 'locationer', 'Mysql Database.', 'Database')
Config.define('MYSQL_USER', 'root', 'Mysql user.', 'Database')
Config.define('MYSQL_PASSWORD', '', 'The redis password', 'Database')

Config.define('NUMBER_OF_FORKS', multiprocessing.cpu_count(), 'Number of forks to use for tornado process. Defaults to number of cpus.', 'Runtime')

Config.define('STATIC_URL', '/static/', 'Static files route.', 'Static')


if __name__ == '__main__':
    generate_config()
