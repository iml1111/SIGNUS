from modules.crawler.list.url_list import List
from pymongo import MongoClient

def init_url_collection(db):
	#soojle 라는 데이터베이스에 접근

	#존재유무 파악
	collist = db.list_collection_names()
	if 'url' in collist:
		print(":::: url ALREADY EXISTS! ::::")
		return

	for component in List:
		query = {
			"url": component['url'],
			"info": component['info'],
			"title_tag": component['title_tag'],
			"login": component['login'],
			"crawling": True,
			"stay_guideline": 0,
			"stay_cnt": 0
		}
		if "post_url" in component:
			query["post_url"] = component['post_url']
		db.url.insert_one(query)
	print(":::: url CREATE Complete! ::::")