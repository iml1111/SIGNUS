'''
MongoDB search_log Collection Model
'''
from flask import current_app
from datetime import timedelta, datetime


class SearchLog:
    """SIGNUS DB search_log Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['search_log']

    def insert_one(self, post_obj):
        ''' 공지사항 추가 '''
        self.col.insert_one(post_obj)
        return True
