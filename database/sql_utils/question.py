# -*- coding: utf-8 -*-

from tornado import gen

from database.tornado_mysql import escape_string
from database.sql_utils.connect import async_connect
from database.nosql_utils.connect import redis_connect


@gen.coroutine
def get_paged_questions(page_count=10, last_qid=None, pre=False):
    conn = yield async_connect()
    cur = conn.cursor()
    if not pre:  # 前页
        if not last_qid:
            sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid ORDER BY qid DESC LIMIT 0, %d;" % page_count
        else:
            sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid WHERE qid<%d ORDER BY qid DESC LIMIT %d;" % (last_qid, page_count)
    else:  # 后页
        if not last_qid:
            return []
        else:
            sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid WHERE qid>=%d ORDER BY qid DESC LIMIT %d;" % (last_qid, page_count)

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
def get_all_tags():
    conn = yield async_connect()
    cur = conn.cursor()
    sql = "SELECT tid, tag_name FROM t_tag ORDER BY tid;"
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
def create_question(tid, username, abstract, content):
    conn = yield async_connect()
    cur = conn.cursor()
    if isinstance(content, str):
        content = escape_string(content)

    sql1 = "INSERT INTO t_question (abstract, content, uid, tid) VALUES ('%s', '%s', (SELECT uid FROM t_user WHERE username='%s'), %d);" % (abstract, content, username, tid)
    sql2 = "SELECT LAST_INSERT_ID() as qid FROM t_question;"
    try:
        data = yield cur.execute(sql1)
        yield cur.execute(sql2)
        last_insert = cur.fetchone()
    except Exception as e:
        data = 0
        last_insert = {}
    finally:
        cur.close()
        conn.close()
    raise gen.Return((data, last_insert.get('qid', None)))


@gen.coroutine
def get_question_by_qid(qid):
    conn = yield async_connect()
    cur = conn.cursor()
    sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, q.created_at, q.updated_at, u.username, t.tag_name FROM t_question AS q LEFT JOIN t_user as u ON u.uid=q.uid LEFT JOIN t_tag as t ON q.tid=t.tid WHERE qid=%d;" % qid
    try:
        yield cur.execute(sql)
        data = cur.fetchone()
    except Exception as e:
        data = {}
    finally:
        cur.close()
        conn.close()

    raise gen.Return(data)


@gen.coroutine
def get_question_by_str(s):
    conn = yield async_connect()
    cur = conn.cursor()
    sql = "SELECT q.qid, q.abstract, q.view_count, q.answer_count, q.created_at, q.updated_at, u.username, t.tag_name FROM t_question AS q "
    sql += "LEFT JOIN t_user as u ON u.uid=q.uid LEFT JOIN t_tag as t ON q.tid=t.tid WHERE username LIKE '%{}%' OR content LIKE '%{}%';".format(s, s)
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
def check_user_has_read(user, qid):
    redis = redis_connect()
    redis.connect()

    conn = yield async_connect()
    cur = conn.cursor()
    has_read = yield gen.Task(redis.sismember, 'user:has:read:%d' % qid, user)
    if has_read:
        data = 0
        raise gen.Return(data)
    redis.sadd('user:has:read:%d' % qid, user)
    sql = "UPDATE t_question SET view_count = view_count + 1 WHERE qid = %d" % qid
    try:
        data = yield cur.execute(sql)
    except Exception as e:
        data = 0
    finally:
        cur.close()
        conn.close()
    raise gen.Return(data)
