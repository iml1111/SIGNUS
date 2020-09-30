'''
MongoDB Category Collection Model
'''
from flask import current_app


class Category:
    """SIGNUS DB category Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['category']

    def find_one(self, obj_id, projection=None):
        ''' 특정 Document 반환 '''
        return self.col.find_one(
            {"_id": ObjectId(obj_id)},
            projection
        )

    def find_many(self, projection=None):
        ''' 모든 Document 반환 '''
        return list(self.col.find(
            {},
            projection
        ))
