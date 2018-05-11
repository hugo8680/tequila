# -*- coding: utf-8 -*-

from database.connect import Connect


def get_paged_questions(page_count=10, last_qid=None, pre=False):
    conn = Connect()
    if not pre:  # 前页
        if not last_qid:
            sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid ORDER BY qid DESC LIMIT 0, %d;" % page_count
        else:
            sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid WHERE qid<%d ORDER BY qid DESC LIMIT %d;" % (last_qid, page_count)
    else:
        if not last_qid:
            return []
        else:
            sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid WHERE qid>=%d ORDER BY qid DESC LIMIT %d;" % (last_qid, page_count)

    try:
        conn.dict_cusor.execute(sql)
        data = conn.dict_cusor.fetchall()
    except Exception as e:
        data = []

    return data