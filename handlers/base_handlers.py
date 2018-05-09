# -*- coding: utf-8 -*-

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('auth-user')

    def get(self, *args, **kwargs):
        self.write('OK')

    def post(self, *args, **kwargs):
        self.write('OK')