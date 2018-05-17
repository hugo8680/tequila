# -*- coding: utf-8 -*-

import json

from tornado import gen
from tornado import web

from handlers.base_handlers import BaseHandler
from database.sql_utils.answer import get_answers, create_answer, get_answer_status
from database.nosql_utils.connect import redis_connect
from database.nosql_utils.channels import ANSWER_STATUS_CHANNEL

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
        self.json_response(200, 'OK', {
            'answer_list': data,
        })


class AnswerCreateHandler(BaseHandler):
    def initialize(self):
        self.redis = redis_connect()
        self.redis.connect()

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
        answer_status = yield get_answer_status(user)

        if not data:
            self.json_response(*CREATE_ERR)
            raise gen.Return()
        yield gen.Task(self.redis.publish, ANSWER_STATUS_CHANNEL, json.dumps(answer_status))
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


class AnswerStatusHandler(BaseHandler):
    def initialize(self):
        self.redis = redis_connect()
        self.redis.connect()

    @web.asynchronous
    def get(self, *args, **kwargs):
        if self.request.connection.stream.closed():
            raise gen.Return()
        self.register()  # 注册回调函数

    @gen.engine
    def register(self):  # 订阅消息
        yield gen.Task(self.redis.subscribe, ANSWER_STATUS_CHANNEL)
        self.redis.listen(self.on_response)

    def on_response(self, data):
        if data.kind == 'message':
            try:
                self.write(data.body)
                self.finish()
            except Exception as e:
                pass
        elif data.kind == 'unsubscribe':
            self.redis.disconnect()

    def on_connection_close(self):
        self.finish()
