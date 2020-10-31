'''
API Main Decorator
'''
from functools import wraps
from time import time
from flask import current_app, g
from app.models.mongodb.user import User
from flask_jwt_extended import verify_jwt_in_request, verify_jwt_in_request_optional, get_jwt_identity


def timer(func):
    '''API 시간 측정 데코레이터'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        process_time = time()
        result = func(*args, **kwargs)
        g.process_time = time() - process_time

        if current_app.config['DEBUG']:
            if isinstance(result, tuple):
                result[0]['process_time'] = g.process_time
            else:
                result['process_time'] = g.process_time

        return result
    return wrapper


def login_optional(func):
    '''토큰 검증(optional) 데코레이터'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request_optional()
        user_id = get_jwt_identity()
        if user_id:
            model = User(g.mongo_cur)
            user_info = model.find_one(user_id)
            if not user_info:
                return {"msg": "Bad Access Token"}, 401
            g.user = user_info
        result = func(*args, **kwargs)
        return result
    return wrapper


def login_required(func):
    '''토큰 검증 데코레이터'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        model = User(g.mongo_cur)
        user_info = model.find_one(user_id)
        if not user_id or not user_info:
            return {"msg": "Bad Access Token"}, 401
        g.user = user_info
        if user_id == current_app.config['ADMIN_ID']:
            g.user['admin'] = True
        else:
            g.user['admin'] = False
        result = func(*args, **kwargs)
        return result
    return wrapper
