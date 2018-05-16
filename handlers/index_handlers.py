# -*- coding: utf-8 -*-

from tornado import gen

from handlers.base_handlers import BaseHandler


class IndexHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render('index.html')