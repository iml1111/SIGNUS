'''
MongoDB user Collection Model
'''
from flask import current_app
from bson.objectid import ObjectId


class User:
    """SIGNUS DB user Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['user']

    def insert_one(self, user_obj):
        ''' 유저 추가 '''
        self.col.insert_one(user_obj)
        return True

    def find_one(self, user_id, projection=None):
        ''' 특정 유저 반환 '''
        return self.col.find_one(
            {"user_id": user_id},
            projection
        )

    def find_many(self, projection=None):
        ''' 모든 유저 반환 '''
        return list(self.col.find(
            {},
            projection
        ))
    
    def find_gt_updated_at(self, updated_time, projection=None):
        ''' updated_time(관심도 측정 시간)보다 
            이후인 유저 반환 '''
        return list(self.col.find(
            {"updated_at": {"$gt": updated_time}},
            projection
        ))

    def check_fav(self, user_id, post_obj):
        ''' 좋아요 이력 체크 '''
        return self.col.find_one(
            {"user_id": user_id},
            {
                "fav_list":
                {
                    "$elemMatch":
                    {
                        '_id': ObjectId(post_obj)
                    }
                }
            }
        )

    def update_one(self, user_id, update_object):
        ''' 특정 사용자의 정보를 update '''
        self.col.update_one(
            {"user_id": user_id},
            {"$set": update_object}
        )
        return True

    def update_list_column_push(self, user_id, _type, _object):
        ''' 특정 리스트(fav/view_list) 컬럼에 정보를 push '''
        self.col.update_one(
            {"user_id": user_id},
            {
                "$push":
                {
                    _type: {"$each": [_object], "$position": 0}
                }
            }
        )
        return True

    def update_list_column_pull(self, user_id, _type, obj_id):
        ''' 특정 리스트(fav/view_list) 컬럼에 정보를 push '''
        self.col.update_one(
            {"user_id": user_id},
            {
                "$pull":
                {
                    _type: {"_id": str(obj_id)}
                }
            }
        )
        return True

    def update_list_pull(self, user_id, _type, push_object):
        ''' 특정 리스트 컬럼에 정보를 pull '''
        self.col.update_one(
            {"user_id": user_id},
            {
                "$pull":
                {
                    _type: {"_id": [push_object], "$position": 0}
                }
            }
        )
        return True

    def remove_one(self, user_id):
        ''' 특정 유저 삭제 '''
        print("not yet")
