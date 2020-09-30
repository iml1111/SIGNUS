'''
SIGNUS V1 newsfeed API
'''
from flask import g, current_app, request
from app.api import input_check
from app.api.signus_v1 import signus_v1 as api
from app.api.decorators import timer, login_optional
from app.controllers.newsfeed import (newsfeed_recommendation,
                                      newsfeed_popularity)


@api.route("/newsfeed/recom", methods=["GET"])
@timer
@login_optional
def signus_v1_recom():
    '''게시글 좋아요 API'''

    if 'user' in g and current_app.config["INDICATORS"]["USER"]["COLD_START"] < g.user["cold_point"]:
        result = newsfeed_recommendation(g.mongo_cur,
                                         g.user,
                                         current_app.config["FT"])
    else:
        result = newsfeed_popularity(g.mongo_cur)

    return {
        "msg": "success",
        "result": result
    }

