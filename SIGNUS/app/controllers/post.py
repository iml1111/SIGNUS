'''
SIGNUS post Controller
'''
from bson import json_util
from app.models.mongodb.posts import Posts


def post_like(mongo_cur, post_oid):
    '''
    게시글 좋아요를 올려주는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > Document ObjectId

    Return
    ---------
    True or False
    '''
    Posts_model = Posts(mongo_cur)
    return Posts_model.update_increase(post_oid, {'fav_cnt': 1, 'popularity': 3})


def post_unlike(mongo_cur, post_oid):
    '''
    게시글 좋아요를 취소하는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > Document ObjectId
    user > user infomation

    Return
    ---------
    True or False
    '''
    Posts_model = Posts(mongo_cur)
    return Posts_model.update_increase(post_oid, {'fav_cnt': -1, 'popularity': -3})

def post_view(mongo_cur, post_oid):
    '''
    게시글 조회수를 올리는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > Document ObjectId

    Return
    ---------
    True or False
    '''
    Posts_model = Posts(mongo_cur)
    return Posts_model.update_increase(post_oid, {'view': 1, 'popularity': 1})
