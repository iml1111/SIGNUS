'''
MongoDB Category Collection Model
'''
from flask import current_app


class Category:
    """SIGNUS DB category Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['category']

    def find_one(self, category_name, projection=None):
        ''' 특정 Document 반환 '''
        return self.col.find_one(
            {"category_name": category_name},
            projection
        )

    def find_many(self, category_list, projection=None):
        ''' 다수 Document 반환 '''
        return list(self.col.find(
            {"category_name": {"$in": category_list}},
            projection
        ))
    
    def find_all(self, projection=None):
        ''' 모든 Document 반환 '''
        return list(self.col.find(
            {},
            projection
        ))
