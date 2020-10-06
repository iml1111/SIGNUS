'''
SIGNUS V1 management API
'''
from flask import g, request
from app.api import input_check
from app.api.signus_v1 import signus_v1 as api
from app.api.decorators import timer, login_required, admin_required
from app.controllers.management import (get_notice,
                                     insert_notice,
                                     update_notice,
                                     delete_notice)


@api.route("/notice")
@api.route("/notice/<string:obj_id>")
@timer
def signus_v1_get_notice(obj_id=None):
    '''공지사항을 반환해주는 API'''
    '''인자가 안들어오면 전체 반환'''
    return {
        "msg": "success",
        "result": get_notice(g.mongo_cur, obj_id)
    }


@api.route("/notice", methods=["PUT"])
@timer
@admin_required
def signus_v1_put_notice():
    '''공지사항 추가 API'''
    data = request.get_json()
    input_check(data, 'title', str)
    input_check(data, 'post', str)

    return {
        "msg": "success",
        "result": insert_notice(g.mongo_cur,
                                data['title'],
                                data['post'])
    }


@api.route("/notice/<string:obj_id>", methods=["PATCH"])
@timer
@admin_required
def signus_v1_patch_notice(obj_id=None):
    '''공지사항 수정 API'''
    data = request.get_json()
    input_check(data, 'title', str)
    input_check(data, 'post', str)

    return {
        "msg": "success",
        "result": update_notice(g.mongo_cur,
                                obj_id,
                                data['title'],
                                data['post'])
    }


@api.route("/notice/<string:obj_id>", methods=["DELETE"])
@timer
@admin_required
def signus_v1_delete_notice(obj_id=None):
    '''공지사항 삭제 API'''
    return {
        "msg": "success",
        "result": delete_notice(g.mongo_cur,
                                obj_id)
    }