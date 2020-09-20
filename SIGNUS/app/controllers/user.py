'''
User Controller Module
'''
import numpy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models.mongodb.user import User


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
    if user_model.find_one(user_id):
        return False
    


    user = {'user_id': user_id,
            'user_pw': generate_password_hash(user_pw),
            'ft_vector': (numpy.zeros(FastText.VEC_SIZE)).tolist()
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
    Get user (유저 정보 반환)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user_id > 아이디

    Return
    ---------
    user_info > 회원 정보
    '''
    user_model = User(mongo_cur)
    return {'user_info': user_model.find_one(user_id)}
