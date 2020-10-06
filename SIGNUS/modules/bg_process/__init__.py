'''
SIGNUS Background process
'''
import sys
from pymongo import MongoClient
from modules.bg_process.measure.interest import interest_run


def user_interest(config):
    '''
    User interest score measurement.
    '''
    cur = MongoClient(config.MONGODB_URI)
    db = cur[config.MONGODB_DB_NAME]

    interest_run(db, config)
    
    cur.close()
    sys.stdout.write("User interest score measurement ... OK\n")


def realtime(config):
    '''
    Realtime update.
    '''
    cur = MongoClient(config.MONGODB_URI)
    db = cur[config.MONGODB_DB_NAME]

    # 실시간 검색어 함수 넣으세요 ! (구현하고)
    
    cur.close()
    sys.stdout.write("Realtime update ... OK\n")
