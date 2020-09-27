'''
SOOJLE 대상으로한 토큰 재생성 파일
실행방법=========================
python3 retokenizer.py <ID> <PW>
================================
<<<<<<< COPYRIGHT. BY NB >>>>>>>
'''
import os
import sys
sys.path.insert(0, "/home/iml/IML_Tokenizer/src/")
sys.path.insert(0, "/home/iml/SOOJLE_Crawler/src/")
sys.path.insert(0, "../")
sys.path.insert(0, "../../../IML_Tokenizer/src/")
from pymongo import MongoClient
from platform import platform
from bson.objectid import ObjectId
from tknizer import *
import time

HOST = 'localhost:27017'

def retokenizer(ID, PW, BOARD):
	client = MongoClient('mongodb://%s:%s@%s' %(ID, PW, HOST))
	db = client["soojle"]
	cnt = 0
	posts_cnt = db[BOARD].find().count()
	posts = db[BOARD].find()
	post_per = 0
	for post in posts:
		cnt += 1
		print(cnt)
		target_id = post["_id"]
		target_token = soojle_tokenize(post["title"], post["post"])
		db[BOARD].update_one({"_id": ObjectId(target_id)}, {"$set": {"token": target_token}})
	print("\n\n:::: ", cnt, " POSTS RETOKENIZING DONE! ::::\n\n")
	client.close()


def retokenizer_everytime(ID, PW, BOARD):
	client = MongoClient('mongodb://%s:%s@%s' %(ID, PW, HOST))
	db = client["soojle"]
	cnt = 0
	posts_cnt = db[BOARD].find().count()
	posts = db[BOARD].find({"info": {"$regex": "everytime"}})
	post_per = 0
	show_percent(post_per)
	for post in posts:
		cnt += 1
		print(cnt)
		target_id = post["_id"]
		target_token = soojle_tokenize(post["title"], post["post"])
		post["token"] = target_token
		del post["_id"]
		del post["title_token"]
		post["title"] = "0"
		db[BOARD].replace_one({"_id": ObjectId(target_id)}, post)
	print("\n\n:::: ", cnt, " POSTS RETOKENIZING DONE! ::::\n\n")
	client.close()

if __name__ == '__main__':
	IS_EVERYTIME = False
	if len(sys.argv) == 4:
		ID = sys.argv[1]
		PW = sys.argv[2]
		BOARD = sys.argv[3]
	elif len(sys.argv) == 5:
		ID = sys.argv[1]
		PW = sys.argv[2]
		if sys.argv[3] == "1" or sys.argv[3] == "True":
			IS_EVERYTIME = True
		BOARD = sys.argv[4]
	else:
		print(":::: WRONG INPUT! ::::\n\n\n")
	if IS_EVERYTIME == True:
		print("POSTS = EVERYTIME")
		time.sleep(3)
		retokenizer_everytime(ID, PW, BOARD)
	else:
		print("POSTS = ALL")
		time.sleep(3)
		retokenizer(ID, PW, BOARD)