from pymongo import MongoClient
from bson.objectid import ObjectId

# 현재 Crawling Site 가 접속이 가능한지 유무 판단해서 true or false 추가
def url_health_check(target_url, db):
	#soojle 라는 데이터베이스에 접근
	target_id = None
	db_url_list = db.url.find({}, {"url":1})
	for db_url in db_url_list:
		if db_url["url"].strip() == target_url.strip():
			target_id = db_url["_id"]
			break
	if target_id == None:
		return
	else:
		target_obj = db.url.find_one({"_id": ObjectId(target_id)})
	if target_obj["stay_cnt"] > 0:
		db.url.update_one({"_id": ObjectId(target_id)}, {"$set": {"stay_cnt": target_obj["stay_cnt"] - 1}})
	else:
		if target_obj['stay_guideline'] < 5:
			target_obj['stay_guideline'] += 1
		db.url.update_one({"_id": ObjectId(target_id)}, {"$set": {"crawling": False, "stay_cnt": 2 ** target_obj['stay_guideline'], "stay_guideline": target_obj['stay_guideline']}})
	print("\n:::: THIS URL CAN NOT CRAWLED! ::::\n")
	
def all_url_Crawling_True(db):
	db.url.update_many({}, {"$set", {"crawling": True, "stay_cnt": 0}})

#Crawling 가능 여부 check
def is_crawling(db, target_crawler):
	print(":::: URL HEALTH CHECKING... ::::")
	try:
		target = db.url.find_one({"info": target_crawler}, {"crawling": 1, "stay_cnt": 1})
		target_id = target["_id"]
	except:
		target_id = None
	if target_id == None:
		print(":::: URL HEALTH DONE! - NONE ::::")
		return True
	if target["crawling"] == False and target["stay_cnt"] == 0:
		db.url.update_one({"_id": ObjectId(target_id)}, {"$set": {"crawling": True, "stay_guideline": 0}})
	elif target["crawling"] == False and target["stay_cnt"] > 0:
		db.url.update_one({"_id": ObjectId(target_id)}, {"$set": {"stay_cnt": target["stay_cnt"] - 1}})
	else:
		print(":::: URL HEALTH DONE! - POSSIBLE ::::")
		return True
	print(":::: URL HEALTH DONE! - IMPOSSIBLE ::::")
	return False