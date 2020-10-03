'''
User Controller Module
'''
import numpy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models.mongodb.user import User
from app.models.mongodb.posts import Posts


def signup(mongo_cur, user_id, user_pw):
    '''
    Sign Up (회원가입 함수)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디
    user_pw > 비밀번호

    Return
    ---------
    token > JWT (String)
    '''
    user_model = User(mongo_cur)
    if user_model.find_one(user_id, {"_id": 0, "user_id": 1}):
        return False
    
    # SJ_AI 대체 임시 변수
    VEC_SIZE = 26
    user = {'user_id': user_id,
            'user_pw': generate_password_hash(user_pw),
            'topic_vector': (numpy.zeros(VEC_SIZE)).tolist(),
            'fav_list': [],
            'view_list': [],
            'newsfeed_list': [],
            'search_list': [],
            'updated_at': datetime.now(),
            'cold_point': 0,
            'created_at': datetime.now()}

    user_model.insert_one(user)
    return True


def signin(mongo_cur, user_id, user_pw):
    '''
    Sign In (로그인 함수)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디
    user_pw > 비밀번호

    Return
    ---------
    token > JWT 문자열(String)
    '''
    user_model = User(mongo_cur)
    user = user_model.find_one(user_id)
    if not user:
        return None
    if not check_password_hash(user['user_pw'], user_pw):
        return None
    return {'access_token': create_access_token(
                identity=user_id, expires_delta=False)}


def get_user(mongo_cur, user_id):
    '''
    Get user infomation (유저 정보 반환)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디

    Return
    ---------
    user_info > 회원 정보
    '''
    user_model = User(mongo_cur)
    return user_model.find_one(user_id, {"_id": 0,
                                         "user_id": 1,
                                         "fav_list": 1,
                                         "view_list": 1,
                                         "newsfeed_list": 1})


def reset_tendency(mongo_cur, user_id):
    '''
    Reset tendency (사용자 관심사 초기화)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디

    Return
    ---------
    result > True or False
    '''
    user_model = User(mongo_cur)
    if user_model.find_one(user_id, {"_id": 0, "user_id": 1}):
        return False
    
    # SJ_AI 대체 임시 변수
    VEC_SIZE = 26
    TOPICS_SZIE = 30
    TEMP_TOPIC = numpy.ones(TOPICS_SZIE)
    user = {'ft_vector': (numpy.zeros(VEC_SIZE)).tolist(),
            'tag': {},
            'tag_sum': 1,
            'tag_vector': (numpy.zeros(VEC_SIZE)).tolist(),
            'topic': (TEMP_TOPIC / TEMP_TOPIC.sum()).tolist(),
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
    result > True or False
    '''
    user_model = User(mongo_cur)
    if user_model.find_one(user_id, {"_id": 0, "user_id": 1}):
        return False
    
    return user_model.update_one(user_id, {"updated_at": datetime.now()})


def fav_push(mongo_cur, obj_id, user):
    '''
    사용자 fav_list에 좋아요 한 게시글을 push

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId
    user > user infomation

    Return
    ---------
    True or False
    '''
    User_model = User(mongo_cur)
    Posts_model = Posts(mongo_cur)

    # 좋아요 중복 체크
    if "fav_list" in User_model.check_fav(user['user_id'], obj_id):
        return False

    # 사용자 좋아요 리스트 캐싱
    post = Posts_model.find_one(obj_id)
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


def fav_pull(mongo_cur, obj_id, user):
    '''
    사용자 fav_list에 좋아요 취소 한 게시글을 pull

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId
    user > user infomation

    Return
    ---------
    True or False
    '''
    User_model = User(mongo_cur)
    Posts_model = Posts(mongo_cur)

    # 좋아요 중복 체크
    if "fav_list" not in User_model.check_fav(user['user_id'], obj_id):
        return False

    # 사용자 좋아요 리스트 캐싱 제거
    post = Posts_model.find_one(obj_id)
    User_model.update_list_column_pull(user['user_id'], "fav_list", post['_id'])
    User_model.update_one(user['user_id'], {"updated_at": datetime.now()})

    return True


def view_push(mongo_cur, obj_id, user):
    '''
    사용자 view_list에 좋아요 한 게시글을 push

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    obj_id > Document ObjectId
    user > user infomation

    Return
    ---------
    True or False
    '''
    User_model = User(mongo_cur)
    Posts_model = Posts(mongo_cur)

    # 사용자 좋아요 리스트 캐싱
    post = Posts_model.find_one(obj_id)
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