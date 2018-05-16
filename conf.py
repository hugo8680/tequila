# -*- coding: utf-8 -*-

import os

DOMAIN = 'http://127.0.0.1:8000'

DEFAULT_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'pics')


SETTINGS = {
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'cookie_secret': 'ee93be7b3b08f4d0f31d16240d352b777f687e57',
    'login_url': '/auth/login',
    'xsrf_token': True,
    'debug': False
}


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