# -*- coding: utf-8 -*-

import base64
import uuid
import hashlib
from io import BytesIO

from tornado import web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from handlers.base_handlers import BaseHandler
from database.auth import get_user_by_username, create_user

from utils.auth_code import get_pic_code
from utils.errcode import LOGIN_VCODE_ERR, PASSWORD_ERR, USERNAME_ERR, USER_EXISTS, USER_CREATE_ERR


class LoginHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render('login.html')

    @run_on_executor
    def post(self, *args, **kwargs):
        sign = self.get_argument('sign', '')
        vcode = self.get_argument('vcode', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        if self.get_secure_cookie(sign).decode('utf-8') != vcode:
            self.json_response(*LOGIN_VCODE_ERR)
            return

        data = get_user_by_username(username)
        if not data:
            self.json_response(*USERNAME_ERR)
            return

        if data.get('password') != hashlib.sha1(password.encode('utf-8')).hexdigest():
            self.json_response(*PASSWORD_ERR)
            return

        self.set_secure_cookie('auth-user', data.get('username', ''))
        self.json_response(200, 'OK', {})

class LogoutHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.clear_cookie('auth-user')
        self.redirect('/?m=注销成功&e=success')

class SignupHandler(BaseHandler):
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render('login.html')

    @run_on_executor
    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        vcode = self.get_argument('vcode', '')
        sign = self.get_argument('sign', '')

        if self.get_secure_cookie(sign).decode('utf-8') != vcode:
            self.json_response(*LOGIN_VCODE_ERR)
            return

        data = get_user_by_username(username)
        if data:
            self.json_response(*USER_EXISTS)
            return

        password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        result = create_user(username, password)
        if not result:
            self.json_response(*USER_CREATE_ERR)
            return

        self.set_secure_cookie('auth-user', username)
        self.json_response(200, 'OK', {})


class AuthCodeHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        b = BytesIO()
        img, check = yield get_pic_code()
        img.save(b, format='png')
        vcode = base64.b64encode(b.getvalue())
        sign = str(uuid.uuid1())
        self.set_secure_cookie(sign, ''.join([str(i) for i in check]).lower(), expires_days=1/48)
        self.json_response(200, 'OK', {
            'vcode': vcode.decode('utf-8'),
            'sign': sign
        })
