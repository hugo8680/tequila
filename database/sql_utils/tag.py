# -*- coding: utf-8 -*-

from tornado import gen

from database.sql_utils.connect import async_connect


@gen.coroutine
def get_tag_list():
    conn = yield async_connect()
    cur = conn.cursor()
    sql = "SELECT tid, tag_name, COUNT(tid) question_count, uid, username, COUNT(uid) user_count FROM ("
    sql += "SELECT q.qid, t.tag_name, t.tid, u.username, u.uid FROM t_question q"
    sql += " LEFT JOIN t_tag t ON t.tid = q.tid"
    sql += " LEFT JOIN t_user u ON u.uid = q.uid) c"
    sql += " GROUP BY tid, uid ORDER BY question_count DESC;"
    try:
        yield cur.execute(sql)
        data = cur.fetchall()
    except Exception as e:
        data = []
    finally:
        cur.close()
        conn.close()
    raise gen.Return(data)