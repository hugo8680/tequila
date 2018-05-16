# -*- coding: utf-8 -*-

from tornado import gen
from tornado import web

from handlers.base_handlers import BaseHandler
from database.answer import get_answers, create_answer

from utils.errcode import PARAMETER_ERR, CREATE_ERR, USER_HAS_NOT_VALIDATE


class AnswerListHandler(BaseHandler):
    @gen.coroutine
    def get(self, qid, *args, **kwargs):
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        data = yield get_answers(qid)
        self.json_response(200, 'OK', {'answer_list': data})


class AnswerCreateHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        qid = self.get_argument('qid', '')
        content = self.get_argument('content', '')
        user = self.current_user

        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()

        if not user:
            self.json_response(*USER_HAS_NOT_VALIDATE)
            raise gen.Return()

        data = yield create_answer(qid, user, content)
        if not data:
            self.json_response(*CREATE_ERR)
            raise gen.Return()
        self.json_response(200, 'OK', {})


class AnswerDetailHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class AnswerUpdateHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class AnswerDeleteHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass
