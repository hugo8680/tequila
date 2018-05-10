# -* coding: utf-8 -*-

from tornado import gen

from database.connect import Connect


def get_user_by_username(username):
    conn = Connect()
    sql = "SELECT username, email, password FROM t_user WHERE username='%s';" % username
    conn.dict_cusor.execute(sql)
    data = conn.dict_cusor.fetchone() or {}
    conn.cursor.close()
    conn.connection.close()
    return data


def create_user(username, password):
    conn = Connect()
    sql = "INSERT INTO t_user(username, password) VALUES ('%s', '%s');" % (username, password)
    data = conn.dict_cusor.execute(sql)
    conn.connection.commit()
    conn.cursor.close()
    conn.connection.close()
    return data