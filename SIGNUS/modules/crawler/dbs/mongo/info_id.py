from pymongo import MongoClient
from modules.crawler.list.url_list import List



def post_info(db):
	
	#soojle 라는 데이터베이스에 접근
	
	#존재유무 파악
	collist = db.list_collection_names()
	if 'post_info' in collist:
		print(":::: post_info ALREADY EXISTS! ::::")
		return

	#info_id : db게시판 테이블에서 보여지는 식별자값
	collection = db["post_info"]
	
	#info_id : sj_domain, title_tag : 도메인, login : 0 추가 ==> example
	collection.insert_one({"info_id": "sj_domain", "title_tag": "도메인/", "info_num": 0})
	print(":::: post_info CREATE Complete! ::::")
	
	#url_list 에서 각 게시판의 info, title_tag, login 값을 post_info 테이블에 넣어준다.
	#login은 로그인 유무
	cnt = 1
	print(List)
	for URL in List:
		collection.insert_one({"info_id": URL['info'], "title_tag": URL['title_tag'], "info_num": cnt})
		cnt+=1
	print(":::: post_info INSERT Complete! ::::")
	
	
	#최신 게시물 저장하는 recent_post 테이블 생성
	collection = db["recent_post"]

	if collection.find().count() == 0:
		for URL in List:
			collection.insert_one({"info_id": URL['info'], "title": 0})
		print(":::: recent_post CREATE Complete! ::::")