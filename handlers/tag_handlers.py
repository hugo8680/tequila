# -*- coding: utf-8 -*-

from tornado import gen


from handlers.base_handlers import BaseHandler
from database.sql_utils.tag import get_tag_list, get_all_tags

from utils.auth import login_required


class TagListHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        data = yield get_tag_list()
        tags = yield get_all_tags()
        self.render('tag_list.html', data={'tag_list': data, 'tags': tags})