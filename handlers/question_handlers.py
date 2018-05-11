# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

from handlers.base_handlers import BaseHandler
from database.question import get_paged_questions

from utils.errcode import PARAMETER_ERR


class QuestionListHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def get(self, *args, **kwargs):
        last_qid = self.get_argument('lqid', None)
        pre = self.get_argument('pre', 0)

        try:
            last_qid = int(last_qid)
        except TypeError:
            last_qid = None

        pre = True if pre == '1' else False
        data = get_paged_questions(page_count=15, last_qid=last_qid, pre=pre)
        lqid = data[-1].get('qid') if data else None

        self.json_response(200, 'OK', {
            'question_list': data,
            'last_qid': lqid
        })


class QuestionCreateHandler(BaseHandler):
    pass


class QuestionDeleteHandler(BaseHandler):
    pass


class QuestionUpdateHandler(BaseHandler):
    pass


class QuestionDetailHandler(BaseHandler):
    pass
