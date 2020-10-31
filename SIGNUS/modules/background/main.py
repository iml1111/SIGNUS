'''
SIGNUS Background process
'''
import sys
from pymongo import MongoClient
from modules.background.src.interest import interest, interest_temp
from modules.background.src.realtime import realtime


def process_interest(config):
    '''
    User interest score measurement.
    '''
    cur = MongoClient(config.MONGODB_URI)
    db = cur[config.MONGODB_DB_NAME]

    interest(db, config)
    
    cur.close()
    sys.stdout.write("User interest score measurement ... OK\n")

# 예외
def process_temp_interest(config):
    '''
    User interest score measurement.
    '''
    cur = MongoClient(config.MONGODB_URI)
    db = cur[config.MONGODB_DB_NAME]

    interest_temp(db, config)
    
    cur.close()
    sys.stdout.write("User interest score measurement ... OK\n")


def process_realtime(config):
    '''
    Realtime update.
    '''
    cur = MongoClient(config.MONGODB_URI)
    db = cur[config.MONGODB_DB_NAME]

    realtime(db, config)
    
    cur.close()
    sys.stdout.write("Realtime update ... OK\n")
