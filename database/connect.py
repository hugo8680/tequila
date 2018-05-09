# -*- coding: utf-8 -*-

import pymysql

from conf import DATABASE


pymysql.install_as_MySQLdb()


def connect():
    config = DATABASE.get('default', {})
    conn = pymysql.connections.Connection(**config)
    return conn.cursor(cursor=pymysql.cursors.DictCursor)
