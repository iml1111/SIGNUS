'''
SIGNUS post Controller
'''
from bson import json_util
from app.models.mongodb.posts import Posts


def post_like(mongo_cur, obj_id):
    '''
    게시글 좋아요를 올려주는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId

    Return
    ---------
    True or False
    '''
    Posts_model = Posts(mongo_cur)
    return Posts_model.update_increase(obj_id, "fav_cnt", 1)


def post_unlike(mongo_cur, obj_id):
    '''
    게시글 좋아요를 취소하는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId
    user > user infomation

    Return
    ---------
    True or False
    '''
    Posts_model = Posts(mongo_cur)
    return Posts_model.update_increase(obj_id, "fav_cnt", -1)

def post_view(mongo_cur, obj_id):
    '''
    게시글 조회수를 올리는 함수

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId

    Return
    ---------
    True or False
    '''
    Posts_model = Posts(mongo_cur)
    return Posts_model.update_increase(obj_id, "view", 1)
