'''
SIGNUS management Controller
'''
from bson.json_util import dumps
from datetime import datetime
from app.models.mongodb.notice import Notice


def get_notice(mongo_cur, obj_id):
    '''
    공지사항 obj_id에 매칭되는 Document를 반환
    (obj_id == None, 전체 반환)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId

    Return
    ---------
    Notice > 공지사항 (Dict or list)
    '''
    Notice_model = Notice(mongo_cur)
    if obj_id:
        return dumps(Notice_model.find_one(obj_id))
    return dumps(Notice_model.find_many())


def insert_notice(mongo_cur, title, post):
    '''
    공지사항 추가

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    title > 제목
    post > 본문

    Return
    ---------
    True or False
    '''
    Notice_model = Notice(mongo_cur)
    return Notice_model.insert_one({"title": title, "post": post, "date": datetime.now()})


def update_notice(mongo_cur, obj_id, title, post):
    '''
    공지사항 수정

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    title > 제목
    post > 본문

    Return
    ---------
    True or False
    '''
    Notice_model = Notice(mongo_cur)
    return Notice_model.update_one(obj_id, {"title": title, "post": post})


def delete_notice(mongo_cur, obj_id):
    '''
    공지사항 obj_id에 매칭되는 Document를 삭제

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId

    Return
    ---------
    True or False
    '''
    Notice_model = Notice(mongo_cur)
    return Notice_model.remove_one(obj_id)