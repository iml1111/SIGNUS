'''
MongoDB Log Collection Model
'''
from flask import current_app


class Log:
    """SIGNUS DB Log Model"""

    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['log']

    def insert_one(self, log_obj):
        ''' insert log '''
        self.col.insert_one(log_obj)
