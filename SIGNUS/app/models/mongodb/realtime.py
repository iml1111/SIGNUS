'''
MongoDB realtime Collection Model
'''
from flask import current_app
from datetime import timedelta, datetime


class Realtime:
    """SIGNUS DB realtime Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['realtime']

    def find_latest(self):
        ''' 최신 실시간 검색어 반환 '''
        return list(self.col.find({},{'_id': 0}).sort([('date', -1)]).limit(1))[0]
