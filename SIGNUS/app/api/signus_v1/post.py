'''
SIGNUS V1 post API
'''
from flask import g
from app.api.signus_v1 import signus_v1 as api
from app.api.decorators import timer, login_required, login_optional
from app.controllers.post import post_like, post_unlike, post_view


@api.route("/post/like/<string:post_oid>", methods=["PATCH"])
@timer
@login_required
def signus_v1_post_like(post_oid):
    ''' 게시글 좋아요 '''
    return {
        "msg": "success",
        "result": post_like(g.mongo_cur,
                            post_oid,
                            g.user)
    }


@api.route("/post/unlike/<string:post_oid>", methods=["PATCH"])
@timer
@login_required
def signus_v1_post_unlike(post_oid):
    ''' 게시글 좋아요 취소 '''
    return {
        "msg": "success",
        "result": post_unlike(g.mongo_cur,
                              post_oid,
                              g.user)
    }


@api.route("/post/view/<string:post_oid>", methods=["PATCH"])
@timer
@login_optional
def signus_v1_post_view(post_oid):
    ''' 게시글 조회수 '''
    if 'user' in g:
        result = post_view(g.mongo_cur, post_oid, g.user)
    else:
        result = post_view(g.mongo_cur, post_oid)
    return {
        "msg": "success",
        "result": result
    }
