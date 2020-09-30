'''
SIGNUS V1 newsfeed API
'''
from flask import g, current_app, request
from app.api import input_check
from app.api.signus_v1 import signus_v1 as api
from app.api.decorators import timer, login_optional
#from app.controllers.newsfeed import ()


@api.route("/newsfeed/recom", methods=["GET"])
@timer
@login_optional
def signus_v1_recom():
    '''게시글 좋아요 API'''

    if 'user' in g and current_app.config["INDICATORS"]["USER"]["COLD_START"] < g.user["cold_point"]:
        result = True
        print(g.user)
        print("회원 추천 뉴스피드")
    
    else:
        print("비회원 추천 뉴스피드")
        result = False

    return {
        "msg": "success",
        "result": result
    }

