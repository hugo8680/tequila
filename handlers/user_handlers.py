# -*- coding: utf-8 -*-

from tornado import gen

from handlers.base_handlers import BaseHandler

from database.sql_utils.user import get_user_list, get_user_by_str

from utils.auth import login_required
from utils.errcode import PARAMETER_ERR


class UserListHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        data = yield get_user_list()
        my_data = {}
        if data:
            for i in data:
                if i.get('username') == self.current_user:
                    my_data = {'username': i.get('username'), 'point': i.get('point'), 'rank': i.get('rank')}
        self.render('user_list.html', data={
            'user_list': data,
            'current_user': my_data
        })


class UserSearchHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        s = self.get_argument('s', '')
        if not 2 <= len(s) <= 12:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()

        data = yield get_user_by_str(s)
        self.json_response(200, 'OK', data={'user_list': data})