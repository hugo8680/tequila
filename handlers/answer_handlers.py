# -*- coding: utf-8 -*-

import json

from tornado import gen
from tornado import web

from handlers.base_handlers import BaseHandler
from database.sql_utils.question import update_question_answer
from database.sql_utils.answer import (get_answers, create_answer, get_answer_status, get_unread_answer, check_answers,
                                       delete_answer_by_id, adopt_answer, add_point, get_adopted_count)
from database.nosql_utils.connect import redis_connect
from database.nosql_utils.channels import ANSWER_STATUS_CHANNEL

from utils.errcode import PARAMETER_ERR, CREATE_ERR, USER_HAS_NOT_VALIDATE, DEL_ERR, ADD_POINT_ERR, ADOPT_COUNT_ERR
from utils.jsonEncoder import JsonEncoder
from utils.auth import login_required


class AnswerListHandler(BaseHandler):
    @gen.coroutine
    def get(self, qid, *args, **kwargs):
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        data = yield get_answers(qid)
        yield check_answers(qid)
        self.json_response(200, 'OK', {
            'answer_list': data,
        })


class AnswerCreateHandler(BaseHandler):
    def initialize(self):
        self.redis = redis_connect()
        self.redis.connect()

    @gen.coroutine
    @login_required
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
        yield gen.Task(self.redis.publish, ANSWER_STATUS_CHANNEL, json.dumps(answer_status, cls=JsonEncoder))
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

    @gen.coroutine
    @login_required
    def post(self, aid, *args, **kwargs):
        qid = self.get_argument('qid', '')
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        try:
            aid = int(aid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()

        user = self.current_user
        result = yield delete_answer_by_id(aid, qid, user)
        up_result = yield update_question_answer(qid)
        if (not result) or (not up_result):
            self.json_response(*DEL_ERR)
            raise gen.Return()
        self.json_response(200, 'OK', {})


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


class AnswerStatusCurrentHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        data = yield get_answer_status(self.current_user)
        self.json_response(200, 'OK', data)


class UnreadAnswerHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        user = self.current_user
        uquestions = yield get_unread_answer(user)
        self.render('unread_answer.html', data={'unread_questions': uquestions})


class AnswerAdoptHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def post(self, aid, *args, **kwargs):
        qid = self.get_argument('qid', '')
        user = self.current_user

        try:
            aid = int(aid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()

        adopted_data = yield get_adopted_count(qid, user)
        if adopted_data.get('adopted_count', 0) >= 3:
            self.json_response(*ADOPT_COUNT_ERR)
            raise gen.Return()

        data = yield adopt_answer(aid, qid)
        if not data:
            self.json_response(*CREATE_ERR)
            raise gen.Return()

        data_point = yield add_point(aid, qid, user)
        if not data_point:
            self.json_response(*ADD_POINT_ERR)
            raise gen.Return()

        self.json_response(200, 'OK', {})
