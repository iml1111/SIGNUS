from modules.crawler.list.url_list import List
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

def init_crawler_collection(db):
	#존재유무 파악
	collist = db.list_collection_names()
	if 'crawler_manager' in collist:
		print(":::: crawler_manager ALREADY EXISTS! ::::")
		return
	else:
		db["crawler_manager"]

	info_list = []			# all
	info_hidden_list = []	# everytime etc..
	for component in List:
		info_list.append(component['info'])
	info_list.remove('sj34_everytime_all')
	info_hidden_list.append('sj34_everytime_all')
	info_hidden_list.append('sig57_campuspick_study')

	query = {
		"is_crawling": False,
		"started_at": datetime.now(),
		"ended_at": datetime.now()
	}
	db.crawler_manager.insert_one(query)
	for hour in range(24):
		if hour == 0:
			post_info_list = info_list + info_hidden_list
		else:
			post_info_list = info_list
		query = {
			"hour": hour,
			"post_info": post_info_list
		}
		db.crawler_manager.insert_one(query)

	print(":::: crawler_manager CREATE Complete! ::::")

def get_crawler_manager(db):
	data = db.crawler_manager.find_one({"is_crawling": {"$exists": True}})
	return data

def get_crawler_timeinfo(db):
	now_hour = datetime.strftime(datetime.now(), "%H")
	data = db.crawler_manager.find_one({"hour": int(now_hour)})
	return data['post_info']

def update_crawler_manager(db, data):
	db.crawler_manager.update_one({"_id": ObjectId(data["_id"])}, {"$set": data})

def Can_crawling(db):
	data = get_crawler_manager(db)
	if data['is_crawling']:
		return False
	return True