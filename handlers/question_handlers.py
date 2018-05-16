# -*- coding: utf-8 -*-

import os
import time
import uuid
import json

from tornado import gen
from tornado import web

from handlers.base_handlers import BaseHandler
from database.question import get_paged_questions, get_all_tags, create_question, get_question_by_qid

from utils.errcode import PARAMETER_ERR, CREATE_ERR
from conf import DEFAULT_UPLOAD_PATH, DOMAIN


class QuestionListHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        last_qid = self.get_argument('lqid', None)
        pre = self.get_argument('pre', 0)

        if last_qid:
            try:
                last_qid = int(last_qid)
            except Exception:
                self.json_response(200, 'OK', {
                    'question_list': [],
                    'last_qid': None
                })

        pre = True if pre == '1' else False
        data = yield get_paged_questions(page_count=15, last_qid=last_qid, pre=pre)
        lqid = data[-1].get('qid') if data else None

        self.json_response(200, 'OK', {
            'question_list': data,
            'last_qid': lqid
        })


class QuestionCreateHandler(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        tags = yield get_all_tags()
        self.render('question_create.html', data={'tags': tags})

    @web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        tag_id = self.get_argument('tag_id', '')
        abstract = self.get_argument('abstract', '')
        content = self.get_argument('content', '')
        user = self.current_user

        try:
            tag_id = int(tag_id)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()

        data, qid = yield create_question(tag_id, user, abstract, content)

        if not data:
            self.json_response(*CREATE_ERR)
            raise gen.Return()

        self.json_response(200, 'OK', {'qid': qid})


class QuestionUploadPicHandler(BaseHandler):
    @web.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.json_response(200, 'OK', {})

    @web.authenticated
    @gen.coroutine
    def post(self, *args, **kwargs):
        pics = self.request.files.get('pic', None)
        urls = []
        if not pics:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        folder_name = time.strftime('%Y%m%d', time.localtime())
        folder = os.path.join(DEFAULT_UPLOAD_PATH, folder_name)
        if not os.path.exists(folder):
            os.mkdir(folder)
        for p in pics:
            file_name = str(uuid.uuid4()) + p['filename']
            with open(os.path.join(folder, file_name), 'wb+') as f:
                f.write(p['body'])
            web_pic_path = 'pics/' + folder_name + '/' + file_name
            urls.append(os.path.join(DOMAIN, web_pic_path))

        self.write(json.dumps({
            'success': True,
            'msg': 'OK',
            'file_path': urls
        }))


class QuestionDeleteHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class QuestionUpdateHandler(BaseHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass


class QuestionDetailHandler(BaseHandler):
    @gen.coroutine
    def get(self, qid, *args, **kwargs):
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()

        data = yield get_question_by_qid(qid)
        self.render('question_detail.html', data={'question': data})
