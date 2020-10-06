'''
MongoDB notice Collection Model
'''
from flask import current_app
from bson.objectid import ObjectId


class Notice:
    """SIGNUS DB notice Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['notice']

    def insert_one(self, notice_obj):
        ''' 공지사항 추가 '''
        self.col.insert_one(notice_obj)
        return True

    def find_one(self, obj_id, projection=None):
        ''' 특정 공지사항 반환 '''
        return self.col.find_one(
            {"_id": ObjectId(obj_id)},
            projection
        )

    def find_many(self, projection=None):
        ''' 모든 공지사항 반환 '''
        return list(self.col.find(
            {},
            projection
        ))

    def update_one(self, obj_id, update_object):
        ''' 특정 공지사항 업데이트 '''
        self.col.update_one(
            {"_id": ObjectId(obj_id)},
            {"$set": update_object}
        )
        return True

    def remove_one(self, obj_id):
        ''' 특정 공지사항 삭제 '''
        self.col.delete_one(
            {"_id": ObjectId(obj_id)}
        )
        return True
