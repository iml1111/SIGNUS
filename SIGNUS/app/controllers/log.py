'''
log Controller Module
'''
from datetime import datetime
from flask import current_app
from app.models.mongodb.log import Log


def insert_log(mongo_cur, user_id, url, method, params=None):
    '''
    Push log (로그 기록 함수)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 사용자 아이디
    url > API 주소
    method > 메소드
    param > 입력 인자

    Return
    ---------
    result > 성공 여부
    '''
    log_model = Log(mongo_cur)

    # url cutting
    if url.startswith("http"):
        url = url.split("/")[3:]
        url = "/" + "/".join(url)

    log_object = {'user_id': user_id,
                  'url': url,
                  'method': method,
                  'params': params,
                  'created_at':datetime.now()}

    if not current_app.config['TESTING']:
        log_model.insert_one(log_object)
