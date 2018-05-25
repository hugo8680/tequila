# -*- coding: utf-8 -*-

import os

DOMAIN = 'http://127.0.0.1:9000'


DEFAULT_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'pics')


DATABASE = {
    'default': {
        'host': 'localhost',
        'port': 3306,
        'database': 'tequila',
        'user': 'root',
        'password': 'woaini',
        'charset': 'utf8'
    }
}


REDIS = {
    'default': {
        'host': 'localhost',
        'port': 6379,
        'password': '',
        'selected_db': 0,
    }
}