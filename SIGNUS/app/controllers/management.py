'''
SIGNUS management Controller
'''
from bson.json_util import dumps
from datetime import datetime
from app.models.mongodb.notice import Notice


def get_notice(mongo_cur, notice_oid):
    '''
    공지사항 notice_oid 매칭되는 Document를 반환
    (notice_oid == None, 전체 반환)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    notice_oid > 공지 ObjectId

    Return
    ---------
    공지 (Dict or list)
    '''
    Notice_model = Notice(mongo_cur)
    if notice_oid:
        notice = Notice_model.find_one(notice_oid)
        notice['author'] = "SIGNUS"
        return dumps(notice)
    return dumps(Notice_model.find_many())


def insert_notice(mongo_cur, title, post, author):
    '''
    공지사항 추가

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    title > 제목
    post > 본문
    author > 작성자

    Return
    ---------
    결과 (Bool)
    '''
    Notice_model = Notice(mongo_cur)
    return Notice_model.insert_one({"title": title, "post": post, "author": author, "date": datetime.now()})


def update_notice(mongo_cur, notice_oid, title, post):
    '''
    공지사항 수정

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    notice_oid > 공지 ObjectId
    title > 제목
    post > 본문

    Return
    ---------
    결과 (Bool)
    '''
    Notice_model = Notice(mongo_cur)
    return Notice_model.update_one(notice_oid, {"title": title, "post": post})


def delete_notice(mongo_cur, notice_oid):
    '''
    공지사항 notice_oid 매칭되는 Document를 삭제

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    notice_oid > 공지 ObjectId

    Return
    ---------
    결과 (Bool)
    '''
    Notice_model = Notice(mongo_cur)
    return Notice_model.remove_one(notice_oid)