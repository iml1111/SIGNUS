'''
Auth Controller Module
'''
from flask import current_app
from numpy import zeros
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from modules.SJ_Auth.sj_auth import sjlms_api, dosejong_api, uis_api
from app.models.mongodb.user import User
from app.models.mongodb.posts import Posts


def auth_sejong(sj_id, sj_pw):
    '''
    세종대학교 구성원 인증 - SJ Auth 사용

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    sj_id > 세종대학교 포털 아이디
    sj_pw > 세종대학교 포털 비밀번호

    Return
    ---------
    True or False (Bool)
    '''
    # 1차 두드림
    result = dosejong_api(sj_id, sj_pw)['result']
    if not result:
        # 2차 세종lms
        result = sjlms_api(sj_id, sj_pw)['result']
        if not result:
            # 3차 세종UIS
            result = uis_api(sj_id, sj_pw)['result']
    
    if result:
        return True
    else:
        return False


def signup(mongo_cur, sj_id, sj_pw, user_id, user_pw, nickname):
    '''
    회원 가입

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    sj_id > 세종대학교 포털 아이디
    sj_pw > 세종대학교 포털 비밀번호
    user_id > 아이디
    user_pw > 비밀번호
    nickname > 닉네임

    Return
    ---------
    access_token > JWT (String)
    '''
    user_model = User(mongo_cur)
    if not auth_sejong(sj_id, sj_pw):
        return False
    if user_model.find_one(user_id, {"_id": 0, "user_id": 1}):
        return False
    user = {'user_id': user_id,
            'user_pw': generate_password_hash(user_pw),
            'nickname': nickname,
            'topic_vector': (zeros(current_app.config["FT_VEC_SIZE"])).tolist(),
            'fav_list': [],
            'view_list': [],
            'newsfeed_list': [],
            'search_list': [],
            'updated_at': datetime.now(),
            'cold_point': 0,
            'created_at': datetime.now()}
    user_model.insert_one(user)
    return {'access_token': create_access_token(identity=user_id, expires_delta=False)}


def signin(mongo_cur, user_id, user_pw):
    '''
    로그인

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디
    user_pw > 비밀번호

    Return
    ---------
    access_token > JWT (String)
    '''
    user_model = User(mongo_cur)
    user = user_model.find_one(user_id)
    if not user:
        return False
    if not check_password_hash(user['user_pw'], user_pw):
        return False
    return {'access_token': create_access_token(identity=user_id, expires_delta=False)}


def secession(mongo_cur, user, user_pw):
    '''
    회원 탈퇴

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user > 사용자 객체
    user_pw > 비밀번호

    Return
    ---------
    True of False > (Bool)
    '''
    user_model = User(mongo_cur)
    if not check_password_hash(user['user_pw'], user_pw):
        return False
    return user_model.delete_one(user['user_id'])


def update_password(mongo_cur, user, old_pw, new_pw, check_pw):
    '''
    비밀번호 변경

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user > 사용자 객체
    old_pw > 이전 비밀번호
    new_pw > 새 비밀번호
    check_pw > 새 비밀번호 확인

    Return
    ---------
    True of False > (Bool)
    '''
    user_model = User(mongo_cur)
    if new_pw != check_pw:
        return False
    if not check_password_hash(user['user_pw'], old_pw):
        return False
    return user_model.update_one(user['user_id'], {'user_pw': generate_password_hash(new_pw)})


def update_nickname(mongo_cur, user, nickname):
    '''
    닉네임 변경

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    nickname > 닉네임 변경

    Return
    ---------
    True of False > (Bool)
    '''
    user_model = User(mongo_cur)
    return user_model.update_one(user['user_id'], {'nickname': nickname})


def get_user(user):
    '''
    유저 정보 반환
    (g.user에 있는 불필요 변수 제거)

    Params
    ---------
    user > 사용자 객체

    Return
    ---------
    사용자 정보 > (Dict)
    '''
    result = user.copy()
    del result['cold_point']
    del result['user_pw']
    del result['created_at']
    del result['updated_at']
    del result['_id']
    del result['topic_vector']
    return result


def fav_push(mongo_cur, post_oid, user):
    '''
    사용자 fav_list에 좋아요 한 게시글을 push

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > 게시글 ObjectId
    user > 사용자 정보

    Return
    ---------
    True of False > (Bool)
    '''
    User_model = User(mongo_cur)
    posts_model = Posts(mongo_cur)
    # 좋아요 중복 체크
    if "fav_list" in User_model.check_fav(user['user_id'], post_oid):
        return False
    # 사용자 좋아요 리스트 캐싱 객체
    post = posts_model.find_one(post_oid)
    fav_object = {
        '_id': str(post['_id']),
        'topic_vector': post['topic_vector'],
        'token': post['token'],
        'post_date': post['date'],
        'title': post['title'],
        'url': post['url'],
        'img': post['img'],
        'date': datetime.now()
    }
    User_model.update_list_column_push(user['user_id'], "fav_list", fav_object)
    User_model.update_one(user['user_id'], {"updated_at": datetime.now()})
    return True


def fav_pull(mongo_cur, post_oid, user):
    '''
    사용자 fav_list에 좋아요 취소 한 게시글을 pull

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > 게시글 ObjectId
    user > 사용자 정보

    Return
    ---------
    True of False > (Bool)
    '''
    User_model = User(mongo_cur)
    posts_model = Posts(mongo_cur)
    # 좋아요 체크
    if "fav_list" not in User_model.check_fav(user['user_id'], post_oid):
        return False
    # 사용자 좋아요 리스트 캐싱 제거
    post = posts_model.find_one(post_oid)
    User_model.update_list_column_pull(user['user_id'], "fav_list", post['_id'])
    User_model.update_one(user['user_id'], {"updated_at": datetime.now()})
    return True


def view_push(mongo_cur, post_oid, user):
    '''
    사용자 view_list에 좋아요 한 게시글을 push

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    post_oid > 게시글 ObjectId
    user > 사용자 정보

    Return
    ---------
    True of False > (Bool)
    '''
    User_model = User(mongo_cur)
    posts_model = Posts(mongo_cur)
    # 사용자 좋아요 리스트 캐싱 객체
    post = posts_model.find_one(post_oid)
    view_object = {
        '_id': str(post['_id']),
        'topic_vector': post['topic_vector'],
        'token': post['token'],
        'post_date': post['date'],
        'title': post['title'],
        'url': post['url'],
        'img': post['img'],
        'date': datetime.now()
    }
    User_model.update_list_column_push(user['user_id'], "view_list", view_object)
    User_model.update_one(user['user_id'], {"updated_at": datetime.now()})
    return True
