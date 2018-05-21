# -*- coding: utf-8 -*-

from tornado.web import StaticFileHandler

from handlers.index_handlers import IndexHandler
from handlers.auth_handlers import LoginHandler, LogoutHandler, SignupHandler, AuthCodeHandler
from handlers.question_handlers import (QuestionListHandler, QuestionCreateHandler, QuestionDeleteHandler,
                                        QuestionUpdateHandler, QuestionDetailHandler, QuestionUploadPicHandler,
                                        QuestionSearchHandler)
from handlers.answer_handlers import (AnswerListHandler, AnswerCreateHandler, AnswerDetailHandler, AnswerUpdateHandler,
                                      AnswerDeleteHandler, AnswerStatusHandler, UnreadAnswerHandler, AnswerStatusCurrentHandler)

from conf import DEFAULT_UPLOAD_PATH


# INDEX
ROUTERS = [
    (r'/', IndexHandler),
    (r'/index', IndexHandler)
]


# USER
ROUTERS += [
]


# AUTH
ROUTERS += [
    (r'/auth/login', LoginHandler),
    (r'/auth/signup', SignupHandler),
    (r'/auth/logout', LogoutHandler),
    (r'/auth/v.img', AuthCodeHandler),
]


# QUESTION
ROUTERS += [
    (r'/question/list', QuestionListHandler),
    (r'/question/create', QuestionCreateHandler),
    (r'/question/update/(\d+)', QuestionUpdateHandler),
    (r'/question/detail/(\d+)', QuestionDetailHandler),
    (r'/question/delelte/(\d+)', QuestionDeleteHandler),
    (r'/question/picload', QuestionUploadPicHandler),
    (r'/question/search', QuestionSearchHandler),
]


# ANSWER
ROUTERS += [
    (r'/answer/list/(\d+)', AnswerListHandler),
    (r'/answer/create', AnswerCreateHandler),
    (r'/answer/update/(\d+)', AnswerUpdateHandler),
    (r'/answer/detail/(\d+)', AnswerDetailHandler),
    (r'/asnwer/delete/(\d+)', AnswerDetailHandler),
    (r'/answer/status', AnswerStatusHandler),
    (r'/answer/status/current', AnswerStatusCurrentHandler),
    (r'/answer/unread', UnreadAnswerHandler),
]


# TAG
ROUTERS += [

]


# STATICFILES
ROUTERS += [
    (r'/pics/(.*?)$', StaticFileHandler, {'path': DEFAULT_UPLOAD_PATH})
]