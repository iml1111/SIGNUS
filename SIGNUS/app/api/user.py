'''
User View Module
'''
from flask import g, request, Blueprint
from app.api import input_check
from app.api.decorators import timer, login_required, login_optional
from app.controllers.user import (signup,
                                  get_user,
                                  signin,
                                  fav_push,
                                  fav_pull,
                                  view_push)


user = Blueprint('user', __name__)


@user.route("/signup", methods=['POST'])
@timer
def api_user_signup():
    ''' 회원 가입 '''
    data = request.get_json()
    input_check(data, "id", str)
    input_check(data, "pw", str)
    return {
        "msg": "success",
        "result": signup(g.mongo_cur,
                         data['id'],
                         data['pw'])
    }


@user.route("/signin", methods=['POST'])
@timer
def api_user_signin():
    ''' 로그인 '''
    data = request.get_json()
    input_check(data, "id", str)
    input_check(data, "pw", str)
    return {
        "msg": "success",
        "result": signin(g.mongo_cur,
                         data['id'],
                         data['pw'])
    }


@user.route("", methods=["GET"])
@timer
@login_required
def api_user_get():
    ''' 회원 정보 반환 '''
    return {
        "msg": "success",
        "result": get_user(g.user)
    }


@user.route("/fav/push/<string:post_oid>", methods=["PUT"])
@timer
@login_required
def api_user_fav_push(post_oid):
    ''' 회원 fav_list에 post 추가 '''
    return {
        "msg": "success",
        "result": fav_push(g.mongo_cur,
                           post_oid,
                           g.user)
    }


@user.route("/fav/pull/<string:post_oid>", methods=["DELETE"])
@timer
@login_required
def api_user_fav_pull(post_oid):
    ''' 회원 fav_list에 post 삭제 '''
    return {
        "msg": "success",
        "result": fav_pull(g.mongo_cur,
                           post_oid,
                           g.user)
    }


@user.route("/view/push/<string:post_oid>", methods=["PUT"])
@timer
@login_required
def api_user_view_push(post_oid):
    ''' 회원 view_list에 post 추가 '''
    return {
        "msg": "success",
        "result": view_push(g.mongo_cur,
                            post_oid,
                            g.user)
    }
