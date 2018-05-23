# -*- coding: utf-8 -*-

from tornado import gen

from handlers.base_handlers import BaseHandler

from utils.auth import admin_required, login_required, superuser_required


class UserListHandler(BaseHandler):
    @gen.coroutine
    @admin_required
    def get(self, *args, **kwargs):
        self.render('user_list.html')