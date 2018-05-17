# -*- coding: utf-8 -*-

from database import tornadoredis

from conf import REDIS


CONF = REDIS.get('default', {})
CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=500,wait_for_available=True)


def redis_connect():
    return tornadoredis.Client(**CONF, connection_pool=CONNECTION_POOL)
