# -*- coding: utf-8 -*-

from tornado.web import StaticFileHandler

from handlers.index_handlers import IndexHandler
from handlers.auth_handlers import LoginHandler, LogoutHandler, SignupHandler, AuthCodeHandler
from handlers.question_handlers import (QuestionListHandler, QuestionCreateHandler, QuestionDeleteHandler,
                                        QuestionUpdateHandler, QuestionDetailHandler, QuestionUploadPicHandler,
                                        QuestionSearchHandler, QuestionFilterHandler)
from handlers.answer_handlers import (AnswerListHandler, AnswerCreateHandler, AnswerDetailHandler, AnswerUpdateHandler,
                                      AnswerDeleteHandler, AnswerStatusHandler, UnreadAnswerHandler, AnswerStatusCurrentHandler,
                                      AnswerAdoptHandler)
from handlers.user_handlers import (UserListHandler, UserSearchHandler)
from handlers.tag_handlers import (TagListHandler,)

from conf import DEFAULT_UPLOAD_PATH


# INDEX
ROUTERS = [
    (r'/', IndexHandler),
    (r'/index', IndexHandler)
]


# USER
ROUTERS += [
    (r'/user/list', UserListHandler),
    (r'/user/search', UserSearchHandler),
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
    (r'/question/delete/(\d+)', QuestionDeleteHandler),
    (r'/question/picload', QuestionUploadPicHandler),
    (r'/question/search', QuestionSearchHandler),
    (r'/question/filter/(\w+)', QuestionFilterHandler),
]


# ANSWER
ROUTERS += [
    (r'/answer/list/(\d+)', AnswerListHandler),
    (r'/answer/create', AnswerCreateHandler),
    (r'/answer/update/(\d+)', AnswerUpdateHandler),
    (r'/answer/detail/(\d+)', AnswerDetailHandler),
    (r'/answer/delete/(\d+)', AnswerDeleteHandler),
    (r'/answer/status', AnswerStatusHandler),
    (r'/answer/status/current', AnswerStatusCurrentHandler),
    (r'/answer/unread', UnreadAnswerHandler),
    (r'/answer/adopt/(\d+)', AnswerAdoptHandler),
]


# TAG
ROUTERS += [
    (r'/tag/list', TagListHandler),
]


# STATICFILES
ROUTERS += [
    (r'/pics/(.*?)$', StaticFileHandler, {'path': DEFAULT_UPLOAD_PATH})
]