'''
MongoDB MasterConfig Collection Model
'''
from flask import current_app


class MasterConfig:
    """RAAS DB user Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['master_config']

    def insert_one(self, key, value):
        ''' config 추가 '''
        self.col.insert_one(
            {
                "key": key,
                "value": value
            }
        )
        return True

    def find_one(self, user_id, projection):
        ''' 특정 config 반환 '''
        return self.col.find_one(
            {"user_id": user_id},
            {"_id": 0}
        )

    def find_many(self, projection):
        ''' 모든 config 반환 '''
        return list(self.col.find(
            {},
            projection
        ))

    def update_one(self, key, value):
        self.col.update_one(
            {"key": key},
            {"$set": {"value": value}}
        )
        return True
    
    def reset_default_config(self):
        for config in default_master_config:
            self.col.update_many(
                {"key": config['key']},
                {"$set": {"value": config['value']}}
            )
        return True
