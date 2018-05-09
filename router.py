# -*- coding: utf-8 -*-

from handlers.auth_handlers import LoginHandler, LogoutHandler, SignupHandler
from handlers.question_handlers import QuestionListHandler, QuestionCreateHandler, QuestionDeleteHandler, QuestionUpdateHandler, QuestionDetailHandler
from handlers.answer_handlers import AnswerListHandler, AnswerCreateHandler, AnswerDetailHandler, AnswerUpdateHandler, AnswerDeleteHandler


# USER
ROUTERS = [
    (r'/auth/login', LoginHandler),
    (r'/auth/signup', SignupHandler),
    (r'/auth/logout', LogoutHandler),
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