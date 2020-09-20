'''
MongoDB Management Modules and Models
'''
from datetime import datetime
from pymongo import MongoClient
from flask import g, current_app
from werkzeug.security import generate_password_hash
from default_data import (default_master_config,
                          default_category,
                          default_realtime)


def get_mongo_cur():
    ''' return mongodb cursor'''
    return MongoClient(current_app.config['MONGODB_URI'])


def open_mongo_cur():
    ''' store mongodb cursor in the g'''
    g.mongo_cur = MongoClient(current_app.config['MONGODB_URI'])


def close_mongo_cur():
    ''' pop & close mongodb cursor in the g'''
    mongo_cur = g.pop('mongo_cur', None)
    if mongo_cur:
        mongo_cur.close()


def init_models(config):
    '''mongodb-init function'''
    cur = MongoClient(config.MONGODB_URI)
    db_name = config.MONGODB_DB_NAME
    
    # col = cur[db_name]['master_config']
    # col.update(
    #     {"__author__": "837477"},
    #     {"$set": {"__author__": "837477"}},
    #     upsert=True)

    col = cur[db_name]['master_config']
    master_config = list(col.find())


    col = cur[db_name]['user']
    col.update_one(
        {"user_id": config.ADMIN_ID},
        {
            "$set":{
                "user_id": config.ADMIN_ID,
                "user_pw": generate_password_hash(config.ADMIN_PW),
                "created_at": datetime.now()
            }
        },
        upsert=True)
    cur.close()
