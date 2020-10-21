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
                                  get_user,
                                  fav_push,
                                  fav_pull,
                                  view_push)


auth = Blueprint('auth', __name__)


@auth.route("/sejong", methods=['POST'])
@timer
def api_auth_sejong():
    ''' 세종대학교 구성원 인증 '''
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
    ''' 회원 가입 '''
    data = request.get_json()
    input_check(data, "sj_id", str, 50)
    input_check(data, "sj_pw", str, 100)
    input_check(data, "id", str, 50)
    input_check(data, "pw", str, 100)
    return {
        "msg": "success",
        "result": signup(g.mongo_cur,
                         data['sj_id'],
                         data['sj_pw'],
                         data['id'],
                         data['pw'])
    }


@auth.route("/secession", methods=['DELETE'])
@timer
@login_required
def api_auth_secession():
    ''' 회원 탈퇴 '''
    data = request.get_json()
    input_check(data, "pw", str, 100)
    return {
        "msg": "success",
        "result": secession(g.mongo_cur,
                            g.user,
                            data['pw'])
    }


@auth.route("/signin", methods=['POST'])
@timer
def api_auth_signin():
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


@auth.route("/user", methods=["GET"])
@timer
@login_required
def api_auth_user():
    ''' 회원 정보 반환 '''
    return {
        "msg": "success",
        "result": get_user(g.user)
    }
