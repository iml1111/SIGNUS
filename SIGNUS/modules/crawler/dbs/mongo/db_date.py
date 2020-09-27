from pymongo import MongoClient
from datetime import datetime, timedelta

from modules.crawler.list.date_cut import date_cut_dict_before

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
now_minus = datetime.now() + timedelta(days = -1)
now_minus = now_minus.strftime("%Y-%m-%d %H:%M:%S")

def init_date_collection(db):

	#존재유무 파악
	collist = db.list_collection_names()
	if 'target_expire' in collist:
		print(":::: target_expire ALREADY EXISTS! ::::")
		return

	for date_one in date_cut_dict_before.items():
		query = {
			"crawler": date_one[0],
			"expire_date": date_one[1]
		}
		db.target_expire.insert_one(query)
	print(":::: date CREATE Complete! ::::")