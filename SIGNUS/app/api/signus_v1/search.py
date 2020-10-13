'''
Search View Module
'''
from flask import g, request, Blueprint
from app.api import input_check
from app.api.signus_v1 import signus_v1 as api
from app.api.decorators import timer
from app.controllers.search import v1_search


@api.route("/search", methods=['POST'])
@timer
def api_search():
    '''search'''
    data = request.get_json()
    input_check(data, "keywords", str)
    input_check(data, "order", str)

    return {
        "msg": "success",
        "result": v1_search(g.mongo_cur,
                            data['keywords'],
                            data['order'])
    }
