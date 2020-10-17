'''
Auth Controller Module
'''
from flask import current_app
from numpy import zeros
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models.mongodb.user import User
from app.models.mongodb.posts import Posts


def signup(mongo_cur, user_id, user_pw):
    '''
    SignUp (회원가입)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디
    user_pw > 비밀번호

    Return
    ---------
    JWT (String)
    '''
    user_model = User(mongo_cur)

    if user_model.find_one(user_id, {"_id": 0, "user_id": 1}):
        return False

    user = {'user_id': user_id,
            'user_pw': generate_password_hash(user_pw),
            'topic_vector': (zeros(current_app.config["FT_VEC_SIZE"])).tolist(),
            'fav_list': [],
            'view_list': [],
            'newsfeed_list': [],
            'search_list': [],
            'updated_at': datetime.now(),
            'cold_point': 0,
            'created_at': datetime.now()}
    user_model.insert_one(user)
    return {'access_token': create_access_token(identity=user_id,
                                                expires_delta=False)}


def signin(mongo_cur, user_id, user_pw):
    '''
    SignIn (로그인 함수)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디
    user_pw > 비밀번호

    Return
    ---------
    JWT (String)
    '''
    user_model = User(mongo_cur)

    user = user_model.find_one(user_id)
    if not user:
        return None
    if not check_password_hash(user['user_pw'], user_pw):
        return None
    return {'access_token': create_access_token(identity=user_id,
                                                expires_delta=False)}


def get_user(user):
    '''
    유저 정보 반환
    (g.user에 있는 불필요 변수 제거)

    Params
    ---------
    user > 사용자 객체

    Return
    ---------
    사용자 정보 (Dict)
    '''
    result = user.copy()
    del result['cold_point']
    del result['user_pw']
    del result['created_at']
    del result['updated_at']
    del result['_id']
    del result['topic_vector']
    return result

def reset_tendency(mongo_cur, user_id):
    '''
    Reset tendency (사용자 관심사 초기화)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디

    Return
    ---------
    결과 (Bool)
    '''
    user_model = User(mongo_cur)

    if user_model.find_one(user_id, {"_id": 0, "user_id": 1}):
        return False

    user = {'topic_vector': (zeros(current_app.config["FT_VEC_SIZE"])).tolist(),
            'fav_list': [],
            'view_list': [],
            'newsfeed_list': [],
            'search_list': [],
            'updated_at': datetime.now(),
            'cold_point': 0}
    return user_model.update_one(user_id, user)


def update_updated_at(mongo_cur, user_id):
    '''
    Update user updated_at time (사용자 액션 시간 갱신)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디

    Return
    ---------
    결과 (Bool)
    '''
    user_model = User(mongo_cur)

    if user_model.find_one(user_id, {"_id": 0, "user_id": 1}):
        return False
    return user_model.update_one(user_id, {"updated_at": datetime.now()})


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
    결과 (Bool)
    '''
    User_model = User(mongo_cur)
    Posts_model = Posts(mongo_cur)

    # 좋아요 중복 체크
    if "fav_list" in User_model.check_fav(user['user_id'], post_oid):
        return False

    # 사용자 좋아요 리스트 캐싱 객체
    post = Posts_model.find_one(post_oid)
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
    결과 (Bool)
    '''
    User_model = User(mongo_cur)
    Posts_model = Posts(mongo_cur)

    # 좋아요 체크
    if "fav_list" not in User_model.check_fav(user['user_id'], post_oid):
        return False

    # 사용자 좋아요 리스트 캐싱 제거
    post = Posts_model.find_one(post_oid)
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
    결과 (Bool)
    '''
    User_model = User(mongo_cur)
    Posts_model = Posts(mongo_cur)

    # 사용자 좋아요 리스트 캐싱 객체
    post = Posts_model.find_one(post_oid)
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