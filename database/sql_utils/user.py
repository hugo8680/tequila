# -*- coding: utf-8 -*-

from tornado import gen

from database.sql_utils.connect import async_connect


@gen.coroutine
def get_user_list():
    conn = yield async_connect()
    cur = conn.cursor()
    sql = "SELECT (@r:=@r+1) AS rank, username, point FROM t_user u, (SELECT (@r:=0)) c WHERE u.group_type = 0 ORDER BY u.point DESC LIMIT 50;"
    try:
        yield cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        data = []
    finally:
        cur.close()
        conn.close()
    raise gen.Return(data)


@gen.coroutine
def get_user_by_str(s):
    conn = yield async_connect()
    cur = conn.cursor()
    sql = "SELECT rank, username, point FROM"
    sql += " (SELECT (@r:=@r+1) AS rank, username, point FROM t_user u, (SELECT (@r:=0)) c WHERE u.group_type = 0 ORDER BY u.point DESC) d"
    sql += " WHERE username LIKE BINARY '%{}%';".format(s)
    try:
        yield cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        data = []
    finally:
        cur.close()
        conn.close()
    raise gen.Return(data)