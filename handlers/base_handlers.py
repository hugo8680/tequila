# -*- coding: utf-8 -*-

import json

from tornado.web import RequestHandler

from database.nosql_utils.connect import redis_connect

from utils.jsonEncoder import JsonEncoder


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('auth-user').decode('utf-8') if self.get_secure_cookie('auth-user') else ''

    def render(self, template_name, err='', message='', data=None, **kwargs):
        data = data if isinstance(data, dict) else {}
        data.update({'username': self.current_user})
        err = err or self.get_argument('e', '')
        message = message or self.get_argument('m', '')
        data.update({'err': err})
        data.update({'message': message})
        super(BaseHandler, self).render(template_name, **data)

    def json_response(self, status, message, data=None):
        data = data if isinstance(data, dict) else {}
        json_response = {
            'status': status,
            'message': message,
            'data': data
        }
        self.write(json.dumps(json_response, cls=JsonEncoder))

    def close_redis_connections(self):
        self.redis.disconnect()
