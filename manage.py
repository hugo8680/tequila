# -*- coding: utf-8 -*-

import os
import sys
import socket

from tornado import web, gen, ioloop, httpserver, process, netutil

from router import ROUTERS
from conf import SETTINGS, DATABASE


class Application(web.Application):
    def __init__(self):
        super(Application, self).__init__(ROUTERS, **SETTINGS)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'run':
        app = Application()
        print('Starting server on port 8000...')
        sockets = netutil.bind_sockets(8000, '127.0.0.1', socket.AF_UNSPEC)
        # process.fork_processes(1)
        server = httpserver.HTTPServer(app)
        server.add_sockets(sockets)
        ioloop.IOLoop.current().start()

    elif args[0] == 'dbshell':
        config = DATABASE.get('default', {})
        os.system('mysql -u{user} -p{password} -D{database} -A'.format(
            user=config.get('user', 'root'),
            password=config.get('password', ''),
            database=config.get('database', 'tequila'))
        )

    elif args[0] == 'migrate':
        config = DATABASE.get('default', {})
        init_sql = 'mysql -u{user} -p{password} -D{database} -A < init.sql'.format(
            user=config.get('user', 'root'),
            password=config.get('password', ''),
            database=config.get('database', 'tequila')
        )
        print('Initializing tables to database {}...'.format(config.get('database')))
        os.system(init_sql)
        print('Completed.')

    elif args[0] == 'shell':
        a = os.system('pip list | grep -w "ipython " 1>/dev/null')
        if a:
            print('Installing ipython...')
            os.system('pip install ipython')
        os.system('ipython')

    elif args[0] == 'help':
        print(""" following arguments available:
        <migrate> for migrating tables to your database,
        <shell> for using ipython shell,
        <dbshell> connect current database,
        <run> run a tornado web server.""")

    else:
        print('Arguments Error. using \'help\' get help.')

