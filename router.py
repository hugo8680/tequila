# -*- coding: utf-8 -*-

from handlers.index_handlers import IndexHandler
from handlers.auth_handlers import LoginHandler, LogoutHandler, SignupHandler, AuthCodeHandler
from handlers.question_handlers import QuestionListHandler, QuestionCreateHandler, QuestionDeleteHandler, QuestionUpdateHandler, QuestionDetailHandler
from handlers.answer_handlers import AnswerListHandler, AnswerCreateHandler, AnswerDetailHandler, AnswerUpdateHandler, AnswerDeleteHandler


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
]


# ANSWER
ROUTERS += [
    (r'/answer/list', AnswerListHandler),
    (r'/answer/create', AnswerCreateHandler),
    (r'/answer/update/(\d+)', AnswerUpdateHandler),
    (r'/answer/detail/(\d+)', AnswerDetailHandler),
    (r'/asnwer/delete/(\d+)', AnswerDetailHandler)
]


# TAG
ROUTERS += [

]