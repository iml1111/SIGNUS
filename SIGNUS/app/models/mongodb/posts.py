'''
MongoDB posts Collection Model
'''
from flask import current_app
from bson.objectid import ObjectId
from datetime import timedelta, datetime


class Posts:
    """SIGNUS DB posts Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['posts']

    def insert_one(self, post_obj):
        ''' 공지사항 추가 '''
        self.col.insert_one(post_obj)
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

    def find_recom_posts(self, info_num, default_date, _limit):
        ''' 추천 뉴스피드 전용 '''
        return list(self.col.find(
            {
                '$and':
                [
                    {'info_num': {'$in': info_num_list}},
                    {'end_date': {'$gt': datetime.now()}},
                    {'date': {'$gt': datetime.now() - timedelta(days=default_date)}}
                ]
            }
        ).sort([('date', -1)]).limit(_limit))

    def find_popularity_posts(self, default_date, _limit):
        ''' 인기 뉴스피드 전용 '''
        return list(self.col.find(
            {
                '$and':
                [
                    {'popularity': {'$gte': 0}},
                    {'date': {'$gt': datetime.now() - timedelta(days=default_date)}}
                ]
            }
        ).sort([('popularity', -1)]).limit(_limit))

    def update_one(self, obj_id, update_object):
        ''' 특정 공지사항 업데이트 '''
        self.col.update_one(
            {"_id": ObjectId(obj_id)},
            {"$set": update_object}
        )
        return True
    
    def update_increase(self, obj_id, _type, num):
        ''' 특정 컬럼 증가/감소 '''
        self.col.update_one(
            {"_id": ObjectId(obj_id)},
            {"$inc": {_type: num}}
        )
        return True

    def remove_one(self, obj_id):
        ''' 특정 공지사항 삭제 '''
        self.col.delete_one(
            {"_id": ObjectId(obj_id)}
        )
        return True
