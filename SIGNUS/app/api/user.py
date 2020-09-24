'''
User View Module
'''
from flask import g, request, Blueprint
from app.api import input_check
from app.api.decorators import timer, login_required
from app.controllers.user import (signup,
                                  signin,
                                  fav_push,
                                  fav_pull,
                                  view_push)

user = Blueprint('user', __name__)


@user.route("/signin", methods=['POST'])
def api_user_signin():
    '''Sign In'''
    data = request.get_json()
    input_check(data, "id", str)
    input_check(data, "pw", str)

    return {
        "msg": "success",
        "result": signin(g.mongo_cur,
                         data['id'],
                         data['pw'])
    }


@user.route("/fav/push/<string:obj_id>", methods=["PUT"])
@timer
@login_required
def api_user_fav_push(obj_id):
    '''fav_list에 post 추가 API'''

    return {
        "msg": "success",
        "result": fav_push(g.mongo_cur,
                           obj_id,
                           g.user)
    }


@user.route("/fav/pull/<string:obj_id>", methods=["DELETE"])
@timer
@login_required
def api_user_fav_pull(obj_id):
    '''fav_list에 post 삭제 API'''

    return {
        "msg": "success",
        "result": fav_pull(g.mongo_cur,
                           obj_id,
                           g.user)
    }


@user.route("/view/push/<string:obj_id>", methods=["PUT"])
@timer
@login_required
def api_user_view_push(obj_id):
    '''view_list에 post 추가 API'''

    return {
        "msg": "success",
        "result": view_push(g.mongo_cur,
                            obj_id,
                            g.user)
    }