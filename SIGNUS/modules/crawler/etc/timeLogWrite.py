from datetime import datetime
from platform import platform
from pymongo import MongoClient
from bson.objectid import ObjectId
import copy
import os

def log_write(start_time, end_time, db, BEFORE_DATA):
	# 로그 파일 열기
	f = open(os.getenv("SIGNUS_CRAWLER_LOG_PATH"),'a')



	# Data 분류
	running_time = end_time - start_time
	posts_data = db.posts.find().count()					# Post Collction 1 포스트 개수
	hidden_posts_data = db.hidden_posts.find().count()		# Post Collction 2 포스트 개수
	all_data = posts_data + hidden_posts_data				# 전체 포스트 개수
	# posts Group By "info"
	classification_to_posts = db.posts.aggregate([
									{"$group": {"_id": "$info", "count": {"$sum": 1}}}
								])
	classification_to_posts = list(classification_to_posts)
	# hidden_posts Group By "info"
	classification_to_hidden = db.hidden_posts.aggregate([
									{"$group": {"_id": "$info", "count": {"$sum": 1}}}
								])
	classification_to_hidden = list(classification_to_hidden)
	classification_all = classification_to_posts + classification_to_hidden
	crawling_classification_all = copy.deepcopy(classification_all)
	for one in crawling_classification_all:
		before_cnt = list(filter(lambda x: one['_id'] == x['_id'], BEFORE_DATA['classification_all']))
		if (len(before_cnt) != 0):
			one['count'] = one['count'] - before_cnt[0]['count']
	classification_crawling_sort = list(filter(lambda x: x['count'] != 0, crawling_classification_all))
	classification_crawling_sort.sort(key=lambda cnt: cnt['count'] ,reverse=True)
	classification_all.sort(key=lambda cnt: cnt['count'] ,reverse=True)
	# Category info Get
	category_all = db.SJ_CATEGORY.find({}, {"_id": False, "category_name": True, "info": True})
	category_all = list(category_all)
	# Crawling Category
	for category in category_all:
		category['info'] = list(map(lambda x: x.split("_")[1] + "_" + x.split("_")[2] if len(x.split("_"))>1  else x, category['info']))
		category['count'] = 0
	category_total = copy.deepcopy(category_all)
	for info_crawling in classification_crawling_sort:
		for category in category_all:
			if info_crawling['_id'] in category['info']:
				category['count'] += info_crawling['count']
	for category in category_all:
		del category['info']
	category_all = list(filter(lambda x: x['count'] != 0, category_all))
	# Total Category
	for info_data in classification_all:
		for category in category_total:
			if info_data['_id'] in category['info']:
				category['count'] += info_data['count']
	for category in category_total:
		del category['info']


	# Shell 출력
	print("END_DATA : ", all_data)
	print("GET_DATA : ", all_data - (BEFORE_DATA['posts_data'] + BEFORE_DATA['hidden_posts_data']))
	print("RUNNING  : ", running_time)
	print("\n\n\n")


	# 파일 입력
	f_data = "----------------------------\n"
	f_data += ":::: CRAWLING SUCCESSFUL ::::\n"
	f.write(f_data)
	f.close()


	# DB 입력
	log = {
		'ended_at': end_time,
		'running_time': str(running_time),
		"crawling_data": {
			'all': all_data - BEFORE_DATA['all_data'],
			'posts': posts_data - BEFORE_DATA['posts_data'],
			'hidden_posts': hidden_posts_data - BEFORE_DATA['hidden_posts_data']
		},
		"now_data": {
			'all': all_data,
			'posts': posts_data,
			'hidden_posts': hidden_posts_data
		},
		"crawled_info": classification_crawling_sort,
		"info_data": classification_all,
		"category_crawling": category_all,
		"category_data": category_total
	}
	db.crawler_log.update_one({"_id": ObjectId(BEFORE_DATA['target'])}, {"$set": log})






def log_ready(start_time, db):
	# 로그 파일 열기
	f = open(os.getenv("SIGNUS_CRAWLER_LOG_PATH"),'a')

	# Data 분류
	start_time = start_time.strftime("%Y-%m-%d")			# 시작시간
	posts_data = db.posts.find().count()					# Post Collction 1 포스트 개수
	hidden_posts_data = db.hidden_posts.find().count()		# Post Collction 2 포스트 개수
	all_data = posts_data + hidden_posts_data				# 전체 포스트 개수
	# posts Group By "info"
	classification_to_posts = db.posts.aggregate([
									{"$group": {"_id": "$info", "count": {"$sum": 1}}}
								])
	classification_to_posts = list(classification_to_posts)
	# hidden_posts Group By "info"
	classification_to_hidden = db.hidden_posts.aggregate([
									{"$group": {"_id": "$info", "count": {"$sum": 1}}}
								])
	classification_to_hidden = list(classification_to_hidden)
	classification_all = classification_to_posts + classification_to_hidden

	
	# Shell 출력
	print(":::: CRAWLER TIME INFO ::::")
	print("TODAY : ", start_time)
	print("NOW_DATA : ", all_data)
	print("\n\n")


	# 파일 입력
	f_data = "----------------------------\n"
	f_data += "TODAY : " + start_time + "\n"
	f_data += "----------------------------\n"
	f.write(f_data)
	f.close()


	# DB 입력
	log = {
		"started_at": datetime.now(),
	}
	db.crawler_log.insert_one(log)
	log_id = db.crawler_log.find({"started_at": {"$gte": log["started_at"]}}, {"_id": True}).sort("started_at", -1).limit(1)
	log_id = list(log_id)[0]['_id']

	# 반환 데이터
	output = {
		'target': log_id,
		'posts_data': posts_data,
		'hidden_posts_data': hidden_posts_data,
		'all_data': posts_data + hidden_posts_data,
		'classification_all': classification_all
	}
	return output