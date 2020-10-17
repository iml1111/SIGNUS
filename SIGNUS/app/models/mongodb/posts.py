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

    def find_one(self, oid, projection=None):
        ''' 특정 공지사항 반환 '''
        return self.col.find_one(
            {"_id": ObjectId(oid)},
            projection
        )

    def find_many(self, projection=None):
        ''' 모든 공지사항 반환 '''
        return list(self.col.find(
            {},
            projection
        ))

    def find_category_posts(self, info_num, default_date, _limit):
        ''' 추천, 카테고리 뉴스피드에서 사용 '''
        ''' 카테고리에 매칭되는 post 찾기 '''
        ''' 최근 x일 적용 버전 '''
        return list(self.col.find(
            {
                '$and':
                [
                    {'info_num': {'$in': info_num}},
                    {'end_date': {'$gt': datetime.now()}},
                    {'date': {'$gt': datetime.now() - timedelta(days=default_date)}}
                ]
            },
            {
                'title': 1,
                'post': 1,
                'img': 1,
                'fav_cnt': 1,
                'view': 1,
                'url': 1,
                'date': 1,
                'end_date': 1,
                'topic_vector': 1,
                'popularity': 1
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
            },
            {
                'title': 1,
                'post': 1,
                'img': 1,
                'fav_cnt': 1,
                'view': 1,
                'url': 1,
                'date': 1,
                'end_date': 1
            }
        ).sort([('popularity', -1)]).limit(_limit))

    def search_posts(self, keyword, tokens, _limit):
        '''검색 전용'''
        return list(self.col.find(
            {
                '$or':
                [
                    {'title': {'$regex': keyword}},
                    {'token': {'$in': tokens}}
                ]
            },
            {
                'title': 1,
                'post': 1,
                'img': 1,
                'fav_cnt': 1,
                'view': 1,
                'url': 1,
                'date': 1,
                'end_date': 1,
                'title_token': 1,
                'token': 1
            }
        ).limit(_limit))

    def update_one(self, oid, update_object):
        ''' 특정 공지사항 업데이트 '''
        self.col.update_one(
            {"_id": ObjectId(oid)},
            {"$set": update_object}
        )
        return True
    
    def update_increase(self, oid, inc_object):
        ''' 특정 컬럼 증가/감소 '''
        self.col.update_one(
            {"_id": ObjectId(oid)},
            {"$inc": inc_object}
        )
        return True

    def remove_one(self, oid):
        ''' 특정 공지사항 삭제 '''
        self.col.delete_one(
            {"_id": ObjectId(oid)}
        )
        return True
