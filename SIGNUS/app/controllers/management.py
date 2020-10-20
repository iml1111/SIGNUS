'''
SIGNUS management Controller
'''
from bson.json_util import dumps
from datetime import datetime
from app.models.mongodb.realtime import Realtime
from app.models.mongodb.notice import Notice


def get_realtime(mongo_cur):
    '''
    최신 실시간 검색어 반환

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object

    Return
    ---------
    실시간 검색어 (list)
    '''
    realtime_model = Realtime(mongo_cur)
    return realtime_model.find_latest()


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
    notice_model = Notice(mongo_cur)
    if notice_oid:
        notice = notice_model.find_one(notice_oid)
        return dumps(notice)
    return dumps(notice_model.find_all())


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
    notice_model = Notice(mongo_cur)
    return notice_model.insert_one({"title": title, "post": post, "author": author, "date": datetime.now()})


def update_notice(mongo_cur, notice_oid, title, post, user_id):
    '''
    공지사항 수정

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    notice_oid > 공지 ObjectId
    title > 제목
    post > 본문
    user_id > 요청 한 사용자 아이디

    Return
    ---------
    결과 (Bool)
    '''
    notice_model = Notice(mongo_cur)
    notice = notice_model.find_one(notice_oid)
    if notice['author'] != user_id:
        return False
    return notice_model.update_one(notice_oid, {"title": title, "post": post})


def delete_notice(mongo_cur, notice_oid, user_id):
    '''
    공지사항 notice_oid 매칭되는 Document를 삭제

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    notice_oid > 공지 ObjectId
    user_id > 요청 한 사용자 아이디

    Return
    ---------
    결과 (Bool)
    '''
    notice_model = Notice(mongo_cur)
    notice = notice_model.find_one(notice_oid)
    if notice['author'] != user_id:
        return False
    return notice_model.remove_one(notice_oid)