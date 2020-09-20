'''
USER View Module
'''
from flask import g, request, Blueprint
from app.api import input_check
from app.controllers.user import (signup,
                                  signin)

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
