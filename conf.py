# -*- coding: utf-8 -*-

import os


SETTINGS = {
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "statics")
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