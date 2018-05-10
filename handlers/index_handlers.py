# -*- coding: utf-8 -*-

from handlers.base_handlers import BaseHandler


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        message = self.get_argument('m', '')
        err = self.get_argument('e', '')

        self.render('index.html', message=message, err=err)