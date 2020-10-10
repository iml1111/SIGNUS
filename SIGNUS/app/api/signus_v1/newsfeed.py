'''
SIGNUS V1 newsfeed API
'''
from flask import g, request, current_app
from app.api.signus_v1 import signus_v1 as api
from app.api.decorators import timer, login_optional
from app.controllers.newsfeed import (newsfeed_recommendation,
                                      newsfeed_popularity,
                                      newsfeed_categroy)


@api.route("/newsfeed/recom", methods=["GET"])
@timer
@login_optional
def signus_v1_recom():
    ''' 추천 뉴스피드 '''
    if 'user' in g and current_app.config["INDICATORS"]["COLD_START"] < g.user["cold_point"]:
        result = newsfeed_recommendation(g.mongo_cur,
                                         g.user)
    else:
        result = newsfeed_popularity(g.mongo_cur)
    return {
        "msg": "success",
        "result": result
    }


@api.route("/newsfeed/popular", methods=["GET"])
@timer
def signus_v1_popular():
    ''' 인기 뉴스피드 '''
    return {
        "msg": "success",
        "result": newsfeed_popularity(g.mongo_cur)
    }


@api.route("/newsfeed/<string:category>", methods=["GET"])
@timer
def signus_v1_category(category):
    ''' 카테고리 뉴스피드 '''
    if category not in {'대학교', '동아리-모임', '공모전-행사', '진로-구인'}:
        abort(400, description="'%s' is not category value" % (category))
    return {
        "msg": "success",
        "result": newsfeed_categroy(g.mongo_cur,
                                    category)
    }
