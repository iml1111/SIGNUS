from modules.crawler import MONGODB_HOST
from modules.crawler import MONGODB_ID
from modules.crawler import MONGODB_PW
from modules.crawler import JWT_SECRET_KEY

from modules.crawler.login.all_login import mongo

from pymongo import MongoClient
from platform import platform

import os

#DB 및 Database 연결
def connect_db():
	#soojle 라는 데이터베이스에 접근
	data = mongo()
	client = MongoClient(os.getenv("SIGNUS_MONGODB_URI"))
	db = client['signus']

	return (client, db)

#DB 연결 해제
def disconnect_db(client):
	client.close()

