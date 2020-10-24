'''
Auth View Module
'''
from flask import g, request, Blueprint
from app.api import input_check
from app.api.decorators import timer, login_required
from app.controllers.auth import (signup,
                                  signin,
                                  auth_sejong,
                                  secession,
                                  update_password,
                                  update_nickname,
                                  get_user)


auth = Blueprint('auth', __name__)


@auth.route("/sejong", methods=['POST'])
@timer
def api_auth_sejong():
    '''세종대학교 구성원 인증'''
    data = request.get_json()
    input_check(data, "sj_id", str, 50)
    input_check(data, "sj_pw", str, 100)
    return {
        "msg": "success",
        "result": auth_sejong(data['sj_id'],
                              data['sj_pw'])
    }


@auth.route("/signup", methods=['POST'])
@timer
def api_auth_signup():
    '''회원 가입'''
    data = request.get_json()
    input_check(data, "sj_id", str, 50)
    input_check(data, "sj_pw", str, 100)
    input_check(data, "id", str, 50)
    input_check(data, "pw", str, 100)
    input_check(data, "nickname", str, 10)
    if (data['nickname'].upper() == "SIGNUS" or
        data['nickname'] == "운영자" or
        data['nickname'] == "관리자"):
        abort(400, description="'%s' Not allowed." % (data['nickname']))

    return {
        "msg": "success",
        "result": signup(g.mongo_cur,
                         data['sj_id'],
                         data['sj_pw'],
                         data['id'],
                         data['pw'],
                         data['nickname'])
    }


@auth.route("/signin", methods=['POST'])
@timer
def api_auth_signin():
    '''로그인'''
    data = request.get_json()
    input_check(data, "id", str)
    input_check(data, "pw", str)
    return {
        "msg": "success",
        "result": signin(g.mongo_cur,
                         data['id'],
                         data['pw'])
    }


@auth.route("/secession", methods=['DELETE'])
@timer
@login_required
def api_auth_secession():
    '''회원 탈퇴'''
    data = request.get_json()
    input_check(data, "pw", str, 100)
    return {
        "msg": "success",
        "result": secession(g.mongo_cur,
                            g.user,
                            data['pw'])
    }


@auth.route("/user/password", methods=['PATCH'])
@login_required
def api_auth_patch_password():
    '''비밀번호 변경'''
    data = request.get_json()
    input_check(data, "old_pw", str, 100)
    input_check(data, "new_pw", str, 100)
    input_check(data, "check_pw", str, 100)
    return {
        "msg": "success",
        "result": update_password(g.mongo_cur,
                                  g.user,
                                  data['old_pw'],
                                  data['new_pw'],
                                  data['check_pw'])
    }


@auth.route("/user/nickname", methods=['PATCH'])
@timer
@login_required
def api_auth_patch_nickname():
    '''닉네임변경'''
    data = request.get_json()
    input_check(data, "nickname", str)
    return {
        "msg": "success",
        "result": update_nickname(g.mongo_cur,
                                  g.user,
                                  data['nickname'])
    }


@auth.route("/user", methods=["GET"])
@timer
@login_required
def api_auth_user():
    '''회원 정보 반환'''
    return {
        "msg": "success",
        "result": get_user(g.user)
    }
