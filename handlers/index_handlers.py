# -*- coding: utf-8 -*-

from tornado import gen

from handlers.base_handlers import BaseHandler

from database.sql_utils.tag import get_all_tags


class IndexHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        tags = yield get_all_tags()
        self.render('index.html', data={'tags': tags})