# -*- coding: utf-8 -*-

from tornado import gen

from database.connect import async_connect


@gen.coroutine
def get_answers(qid):
    conn = yield async_connect()
    cur = conn.cursor()
    sql = "SELECT a.aid, a.status, a.created_at, a.updated_at, a.content, u.username FROM t_answer a LEFT JOIN t_user u ON u.uid=a.uid WHERE qid=%d ORDER BY a.created_at DESC;" % qid
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
def create_answer(qid, user, content):
    conn = yield  async_connect()
    cur = conn.cursor()
    sql = "INSERT INTO t_answer (qid, uid, content) VALUES (%d, (SELECT uid FROM t_user WHERE username='%s'), '%s');" % (qid, user, content)
    try:
        data = yield cur.execute(sql)
    except Exception as e:
        data = 0
    finally:
        cur.close()
        conn.close()
    raise gen.Return(data)