# -*- coding: utf-8 -*-

import pymysql

from conf import DATABASE


pymysql.install_as_MySQLdb()


class Connect(object):
    def __init__(self):
        self.config = DATABASE.get('default', {})
        self.connection = pymysql.connections.Connection(**self.config)
        self.cursor = self.connection.cursor()
        self.dict_cusor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    def close(self):
        self.connection.close()
        self.dict_cusor.close()
        self.cursor.close()



def connect():
    config = DATABASE.get('default', {})
    conn = pymysql.connections.Connection(**config)
    return conn.cursor(cursor=pymysql.cursors.DictCursor)
