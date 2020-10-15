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
@api.route("/notice/<string:notice_oid>")
@timer
def signus_v1_get_notice(notice_oid=None):
    ''' 공지 반환 (인자가 안들어오면 전체 반환) '''
    return {
        "msg": "success",
        "result": get_notice(g.mongo_cur, notice_oid)
    }


@api.route("/notice", methods=["PUT"])
@timer
@admin_required
def signus_v1_put_notice():
    ''' 공지 추가 '''
    data = request.get_json()
    input_check(data, 'title', str)
    input_check(data, 'post', str)
    return {
        "msg": "success",
        "result": insert_notice(g.mongo_cur,
                                data['title'],
                                data['post'])
    }


@api.route("/notice/<string:notice_oid>", methods=["PATCH"])
@timer
@admin_required
def signus_v1_patch_notice(notice_oid=None):
    ''' 공지 수정 '''
    data = request.get_json()
    input_check(data, 'title', str)
    input_check(data, 'post', str)
    return {
        "msg": "success",
        "result": update_notice(g.mongo_cur,
                                notice_oid,
                                data['title'],
                                data['post'])
    }


@api.route("/notice/<string:notice_oid>", methods=["DELETE"])
@timer
@admin_required
def signus_v1_delete_notice(notice_oid=None):
    ''' 공지 삭제 '''
    return {
        "msg": "success",
        "result": delete_notice(g.mongo_cur,
                                notice_oid)
    }