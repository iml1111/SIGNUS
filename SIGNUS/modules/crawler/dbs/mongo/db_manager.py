from pymongo import MongoClient
from modules.crawler.etc.time_convert import datetime_to_mongo
from modules.crawler.etc.time_convert import mongo_to_datetime
from modules.crawler.list import filtering
from modules.crawler.list.url_list import List
from datetime import datetime
import hashlib
from modules.tokenizer import Tokenizer
from modules.recommender.fasttext import Recommender

import os
# Tokenizer 클래스 선언
TK = Tokenizer()

# FT (Recommender) 클래스 선언
FT = open(os.getenv("SIGNUS_FT_MODEL_PATH"))

#md5 해쉬
enc = hashlib.md5()

#POST INFO
POST_INFO = []
#공모전 ~까지를 위한 collum 생성
CONTEST_LIST = ["campuspick_activity", "campuspick_contest", "campuspick_club", "detizen_contest", "detizen_activity", "jobkorea_job", "jobkorea_public", "jobsolution_job", "thinkgood_info", "udream_jobinfo", "dodream_event"]
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_lastly_post(URL, db):
	#soojle 라는 데이터베이스에 접근

	table_name = URL['info']
	document = db.recent_post.find_one({"info_id": table_name})
	if document == None:
		lastly_post_title = 0
	else:
		lastly_post_title = document['title']

	return lastly_post_title

def push_lastly_post(URL, lastly_post_title, db):
	#soojle 라는 데이터베이스에 접근

	table_name = URL['info']
	db.recent_post.update_one({"info_id": table_name}, {'$set': {"title": lastly_post_title}})
	print("\n\n:::: recent_post INSERT Complete! ::::\n\n")


def db_manager(URL, post_data_prepare, db):
	global POST_INFO
	add_cnt = 0
	#table_name = URL['info']
	table_name = "posts"
	temp = []
	#soojle 라는 데이터베이스에 접근

	#게시판에 맞는 테이블 없으면 생성
	##### post_id: 게시물 식별값, title: 제목, author: 작성자, date: 작성일, post: 게시물내용, img: OpenGraph용 url #####
	##### info: 게시판 정보, fav_cnt: 좋아요개수, view: view 개수										 #####
	#post_data_prepare 을 필터링 check를 해준다.
	for post in post_data_prepare:
		if URL['info'].split('_')[0] in ["sj34"]:
			if filtering.filter_public(post['title'] + post['post']):
				print("Unhealty Post ---- ", post['title'])
			elif URL['info'].split('-')[0] == 'sj34':
				if filtering.filter_hardcore(post['title'] + post['post']):
					print("Harmful Post ---- ", post['title'])
				else:
					temp.append(post)
			else:
				temp.append(post)
		else:
			temp.append(post)
	post_data_prepare = temp

	#post_data_prepare 에 값이 없으면 return
	post_data_prepare_len = len(post_data_prepare)
	if post_data_prepare_len == 0:
		return add_cnt

	#입력 포스트를 DB포스트들과 title을 비교하여서 중복되지 않으면 add_cnt++, 중복되면 continue
	#url hashed 값이 같은 게시글이 나오면 continue
	for post_one in post_data_prepare:
		#prepare 게시물이 db 게시물과 비교해서 중복되면 continue
		hash_before = post_one['title'] + post_one['post']
		hash_done = hashlib.md5(hash_before.encode('utf-8')).hexdigest()
		url_hash_before = post_one['url']
		url_hash_done = hashlib.md5(url_hash_before.encode('utf-8')).hexdigest()
		
		# post_one["info"] = URL['info'].split("_")[1] + "_" + URL['info'].split("_")[2]
		post_one["info"] = URL['info']
		for info in POST_INFO:
			if post_one['info'] == info['info_id']:
				post_one['info_num'] = info['info_num']
				break
		# 중복처리====================================================================
		duplicate_check = False
		if db.posts.find_one({"hashed": hash_done}) != None:
			duplicate_check = True
		elif db.posts.find_one({"url_hashed": url_hash_done}) != None:
			duplicate_check = True
		if duplicate_check == True:
			continue
		else:#=============================================================================
			post_one["url_hashed"] = url_hash_done
			post_one["hashed"] = hash_done
			post_one["date"] = datetime_to_mongo(post_one['date'])
			post_one["view"] = 0
			post_one["fav_cnt"] = 0
			if post_one["title"][-3:] == "..." and post_one["post"].startswith(post_one["title"][:-3]):
				post_one["title_token"] = post_one["post"][:20].split(" ")
			else:
				post_one["title_token"] = post_one["title"].split(" ")
			if post_one["post"].startswith(post_one["title"][:-3]):
				post_one["token"] = TK.get_tk(post_one["post"].lower())
			else:
				post_one["token"] = TK.get_tk(post_one["title"].lower() + post_one["post"].lower())
			post_one["token"] = list(URL['title_tag'] + post_one["token"])
			# post_one["login"] = URL["login"]
			del post_one["author"]
			if 'end_date' in post_one.keys():
				#post_one["date"] = datetime_to_mongo(post_one["date"])
				post_one["end_date"] = datetime_to_mongo(post_one["end_date"])
			elif (URL['info'].split("_")[1] + "_" + URL['info'].split("_")[2] in CONTEST_LIST):
				post_one["end_date"] = post_one['date']
				post_one["date"] = datetime_to_mongo(now)
			else:
				post_one["end_date"] = datetime_to_mongo("3000-01-01 00:00:00")
			# 미래시간이면 현재시간 치환
			if post_one['date'] > datetime.now():
				post_one['date'] = datetime.now()
			post_one["title"] = post_one["title"]#[:100]
			post_one["post"] = post_one["post"]#[:200]
			topic = []
			if 'token' in post_one:
				topic_str = post_one["token"]
			else:
				topic_str = []
			post_one["topic_vector"] = FT.doc2vec(topic_str).tolist()
			post_one["popularity"] = 0
			db.posts.insert_one(post_one)
			add_cnt += 1
	return add_cnt

#'info' 의 테이블에 있는 포스트의 개수 반환하는 함수
def get_table_posts(URL, db):
	#soojle 라는 데이터베이스에 접근

	posts_num = db.posts.find().count()

	return posts_num


#한 페이지 안에서 같은 post_data 제거 함수
def sameposts_set(post_data_prepare):
	clear_posts = []
	before_num = len(post_data_prepare)

	#첫번째 post 데이터 넣어주기
	clear_posts.append(post_data_prepare[0])

	for i in range(before_num):
		after_num = len(clear_posts)
		same_cnt = 0
		for j in range(after_num):
			if post_data_prepare[i]['title'] == clear_posts[j]['title']:
				same_cnt += 1
			else:
				continue
		if same_cnt == 0:
			clear_posts.append(post_data_prepare[i])

	return clear_posts

#post_info 리스트 가져오기
def get_post_infoes(db):
	global POST_INFO
	infoes = db.post_info.find({}, {"_id": False, "info_id": True, "info_num": True})
	POST_INFO = []
	for info in infoes:
		try:
			info['info_id'] = info['info_id'].split('_')[1] + '_' + info['info_id'].split('_')[2]
		except:
			pass
		POST_INFO.append(info)
	print(":::: Get Post_info Complete! ::::")
	return True