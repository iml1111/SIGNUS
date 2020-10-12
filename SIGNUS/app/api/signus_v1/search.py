'''
Search View Module
'''
from flask import g, request, Blueprint
from app.api import input_check
from app.api.signus_v1 import signus_v1 as api
from app.controllers.search import v1_search


@api.route("/search", methods=['POST'])
def api_search():
    '''search'''
    data = request.get_json()
    input_check(data, "keyword", str)
    input_check(data, "skip", int)
    input_check(data, "limit", int)
    input_check(data, "order", str)

    return {
        "msg": "success",
        "result": search(g.mongo_cur,
                         data['keyword'],
                         data['skip'],
                         data['limit'],
                         data['order'])
    }
