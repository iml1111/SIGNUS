'''
SIGNUS post Controller
'''
from bson import json_util
from app.models.mongodb.posts import Posts
from app.controllers.auth import (fav_push,
                                  fav_pull,
                                  view_push)

def post_like(mongo_cur, post_oid, user):
    '''
    게시글 좋아요를 올려주는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > 게시글 ObjectId
    user > 사용자 정보

    Return
    ---------
    결과 (Bool)
    '''
    posts_model = Posts(mongo_cur)
    if fav_push(mongo_cur, post_oid, user):
        return posts_model.update_increase(post_oid, {'fav_cnt': 1, 'popularity': 3})
    else:
        return False


def post_unlike(mongo_cur, post_oid, user):
    '''
    게시글 좋아요를 취소하는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > 게시글 ObjectId
    user > 사용자 정보

    Return
    ---------
    결과 (Bool)
    '''
    posts_model = Posts(mongo_cur)
    if fav_pull(mongo_cur, post_oid, user):
        return posts_model.update_increase(post_oid, {'fav_cnt': -1, 'popularity': -3})
    else:
        return False


def post_view(mongo_cur, post_oid, user=None):
    '''
    게시글 조회수를 올리는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > 게시글 ObjectId
    user > 사용자 정보

    Return
    ---------
    결과 (Bool)
    '''
    posts_model = Posts(mongo_cur)
    if user:
        view_push(mongo_cur, post_oid, user)
    return posts_model.update_increase(post_oid, {'view': 1, 'popularity': 1})
