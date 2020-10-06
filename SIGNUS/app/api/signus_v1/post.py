'''
SIGNUS V1 post API
'''
from flask import g, request
from app.api import input_check
from app.api.signus_v1 import signus_v1 as api
from app.api.decorators import timer, login_required
from app.controllers.post import (post_like,
                                  post_unlike,
                                  post_view)


@api.route("/post/like/<string:obj_id>", methods=["PATCH"])
@timer
@login_required
def signus_v1_post_like(obj_id):
    '''게시글 좋아요 API'''

    return {
        "msg": "success",
        "result": post_like(g.mongo_cur,
                            obj_id)
    }


@api.route("/post/unlike/<string:obj_id>", methods=["PATCH"])
@timer
@login_required
def signus_v1_post_unlike(obj_id):
    '''게시글 좋아요 취소 API'''

    return {
        "msg": "success",
        "result": post_unlike(g.mongo_cur,
                              obj_id)
    }


@api.route("/post/view/<string:obj_id>", methods=["PATCH"])
@timer
def signus_v1_post_view(obj_id):
    '''게시글 좋아요 API'''

    return {
        "msg": "success",
        "result": post_view(g.mongo_cur,
                            obj_id)
    }
