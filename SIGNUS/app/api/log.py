'''
Logging View Module
'''
from flask import request, Blueprint, g
from app.controllers.log import insert_log
from app.api.decorators import login_required
from app.api import input_check

log = Blueprint('log', __name__)


@log.route("/page", methods=['PUT'])
@login_required
def api_log_page():
    '''
    페이지 템플릿 접근에 대한 트래킹 API

    Params
    ---------
    url: 접근 페이지 URL (str)
    '''
    data = request.get_json()
    input_check(data, 'url', str)

    insert_log(g.mongo_cur,
               g.user['user_id'],
               data['url'],
               "GET")
    return {}, 204
