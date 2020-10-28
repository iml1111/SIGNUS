
#--------------------공모전 URL--------------------
# sj13_computer_event http://ce.sejong.ac.kr/index.php?mid=contest&page=
# sj15_classic_event http://board.sejong.ac.kr/boardlist.do?bbsConfigFK=810&searchLowItem=&currentPage=
# sig25_thinkgood_info https://www.thinkcontest.com/Contest/CateField.html?s=ing&page=
# sig26_campuspick_activity https://www.campuspick.com/activity
# sig26_campuspick_contest https://www.campuspick.com/contest
# sj30_sejongstation_activity http://cafe484.daum.net/_c21_/bbs_list?grpid=1SVkj&fldid=KObP&lastbbsdepth=000Eozzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&listnum=20&page=
# sj34_everytime_all https://everytime.kr
# sig35_detizen_contest http://www.detizen.com/activity/?Category=3&IngYn=Y&PC=
# sig35_detizen_activity http://www.detizen.com/activity/?Category=3&IngYn=Y&PC=
#-------------------------------------------------

#--------------------tag_names--------------------
# 동아리&모임
#-------------------------------------------------

#-----------------tag_names_board-----------------
# 공모전&대외활동
#-------------------------------------------------

#------------------------info---------------------
# domain_sejong_clubdevelop
# domain_thinkgood_carrer
# domain_campuspick_career
# domain_daum_sejongstation
#-------------------------------------------------
import timeit
from datetime import timedelta
from datetime import datetime
import datetime
import time

from modules.crawler.etc.time_convert import datetime_to_mongo
from modules.crawler.etc.time_convert import mongo_to_datetime
from modules.crawler.list.date_cut import date_cut_dict_before
from modules.crawler.list import filtering
from modules.crawler.dbs.mongo.db_connect import connect_db, disconnect_db
from modules.crawler.list.url_list import List
from modules.crawler.login import campuspick
from modules.tokenizer import Tokenizer
from modules.recommender.fasttext import Recommender

import pymongo
from pymongo import MongoClient

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from platform import platform
import os
import hashlib


TK = Tokenizer()

# FT (Recommender) 클래스 선언 
FT = Recommender(os.getenv("SIGNUS_FT_MODEL_PATH"))

# 속도체크
start_time = 0 
terminate_time = 0

# 교내 공모전 : insideCampus
# 교외 공모전 : outsideCampus
# 데이터 개수 : limit
def getData(db, limit):
	insideCampus = list(db.posts.find({
				"$and": [
					{ "tag": "공모전&대외활동" }, 
					{ "tag": "교내"},
			] 
		}).sort([('date', -1)]).limit(limit))
	outsideCampus = list(db.posts.find({
				"$and":[
					{ "tag": {"$ne":"교내"} }, 
					{ "tag": "공모전&대외활동" } 
			]        
		}).sort([('date', -1)]).limit(limit))
	return insideCampus, outsideCampus

def init_db_date(db):
	# date 값 싹 날려버리기
	date_dict_list = list(db.date.find())
	date_list = []
	for item in date_dict_list:
		date_list.append(item["crawler"])
	for item in date_list:
		db.date.remove({"crawler":item})
	# -------------------------------------------------------------

	# 해당 sj date 날려버리기
	date_list = list(db.date.find({"crawler":"s"}))
	db.date.remove({"crawler":"s"})
	for date in date_list:
		print(date)

# date_cut에 값 넣고 실행하기
def insert_db_date(db):
	date_dict_list = list(db.date.find())
	date_list = []
	for item in date_dict_list:
		date_list.append(item["crawler"])
	
	date_list_before = list(date_cut_dict_before)
	for date in date_list_before:
		if date in date_list:
			pass
		else:		
			query = {
				"crawler": date,
				"date_exp": "2009-01-01 00:00:00"
			}
			db.date.insert_one(query)

#  특정 info 삭제
def remove_db_posts(db):
	# INFO_LIST=["sig26_campuspick_activity","sig50_campuspick_parttime","sig27_campuspick_language","sig26_campuspick_contest","sig28_campuspick_club","sig55_campuspick_job"]
	# for item in INFO_LIST:
	# 	db.posts.remove({"info":item})
	# 	db.recent_post.remove({"info_id":item})
	db.posts.remove({"info":"sig54_naver_news"})
#  posts DB삭제
def drop_db_collection(db):
	INFO_LIST=["thinkgood_info","campuspick_activity","campuspick_contest","campuspick_language",\
		"campuspick_job","campuspick_certificate","campuspick_study","campuspick_club","everytime_all",\
			"detizen_contest","detizen_activity","jobkoreatip_tip","jobkorea_job","jobkorea_public",\
				"rndjob_job","indeed_job","infor_notice","external_notice","review_data","addcampus_board",\
					"20lab_column","20lab_infographics","20lab_announcement","20lab_data","20lab_report",\
						"vms_volunteer","naver_news","campuspick_parttime","univ20_main","kosaf_info"]
	
	posts = db.posts.find({},{"_id":False, "title":True, "date":True, "post":True, "tag":True,\
		"img":True, "url":True, "info":True, "url_hashed":True, "hashed":True, "view":True,\
			"fav_cnt":True, "title_token":True, "token":True, "login":True, "learn":True,\
				"end_date":True, "topic":True, "ft_vector":True, "popularity":True})
	post_list = list(posts)
	post_cnt = len(post_list)
	print("현재 게시글 개수 ::: ", post_cnt)
	
	no_remove_data = []
	remove_data  = []
	
	for post in post_list:
		if post["info"] in INFO_LIST:
			no_remove_data.append(post)
		else :
			remove_data.append(post)
	print("지우면 안되는 데이터 개수 ::: ", len(no_remove_data))
	print("지워야 할 데이터 개수 ::: ", len(remove_data))
	print("합계 ::: ", len(no_remove_data) + len(remove_data))
	if post_cnt == len(no_remove_data) + len(remove_data):
		print("CLEAR")
	
	db.posts.drop()	

	for data in no_remove_data:
		db.posts.insert_one(data)
	
	insert_posts_data = db.posts.count_documents({})
	print("posts collection count ::: ", insert_posts_data)

def drop_all_collection(db):
	db.crawler_log.drop()
	db.crawler_manager.drop()
	db.target_expire.drop()
	db.domain.drop()
	db.recent_post.drop()
	db.post_info.drop()
	db.posts.drop()
	db.tag_info.drop()
	db.url.drop()
	db.category.drop()

def get_post_url(db):
	except_info = ["sj4","sj17","sj19","sj20","sj23","sj30","sj34","sj44","sig56"]
	info_list = []
	none_list = [] #posts가 0개인 url들
	total = 0 
	for url_list in List:
		info_list.append({"info" : url_list['info'],"cnt":0})
	
	for item in info_list:
		crawling_name = item['info'].split("_")[0]
		cnt = db.posts.find({"info":item['info']}).count()
		item['cnt'] = cnt
		if (cnt == 0) and (crawling_name not in except_info):
			none_list.append(item)
		total += cnt
	print("--------------------------------------------------")
	print("--------------------------------------------------")
	print("::::::::::::::::URL별 POST 개수::::::::::::::::")
	for i in info_list:
		print(i['info'] + ' : ', i['cnt'] , '개')
	print("--------------------------------------------------")
	print("--------------------------------------------------\n\n")

	print("POST 총 합 : ",total)
	print("\n\n")

	print("::::::::::::::::::::::::::::::::::::::::::::::::::")
	print("::::::::::::::::posts 0 개인 URL들::::::::::::::::")
	print("::::::::::::::::::::::::::::::::::::::::::::::::::")
	print("::::::::::::::::::::::::::::::::::::::::::::::::::")
	for i in none_list:
    		print(i['info'] + ' : ', i['cnt'] , '개')
	print("::::::::::::::::::::::::::::::::::::::::::::::::::")
	print("::::::::::::::::::::::::::::::::::::::::::::::::::")
	
def test_selenium():
	options = webdriver.ChromeOptions()
	options.add_argument('window-size=1920x1080')
	options.add_argument("disable-gpu")
	options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome")
	options.add_argument("lang=ko_KR")
	driver = webdriver.Chrome("C:/Users/82109/Desktop/SIGNUS/SIGNUS/modules/crawler/chromedriver_86.exe", options=options)
	driver = campuspick.login(driver)


	driver.get('https://www.campuspick.com/job')
	scroll_cnt = 0
	last_height = driver.execute_script("return document.body.scrollHeight")

	while 1:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.badges"))) #div.header을 발견하면 에이작스 로딩이 완료됬다는 가정

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		time.sleep(2)
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
		time.sleep(2)	

		new_height = driver.execute_script("return document.body.scrollHeight")
		
		if new_height == last_height:
			break
		last_height = new_height
		scroll_cnt = scroll_cnt + 1
		print(scroll_cnt)
		if scroll_cnt==20:
			break
	
	html = driver.page_source
	bs = BeautifulSoup(html,'html.parser')
	posts = bs.find("div", {"class": 'list'}).findAll("a", {"class": "top"})
	print("포스트 개수 : ",len(posts))

# post와 info_num 매칭 함수
def matching_info_num(db):
	for url in List:
		info = url['info']
		each_posts = list(db.posts.find({"info":info},{"_id":1})) #각각의 url별 모든 게시글 들을 가져온다.
		each_info_num = db.post_info.find_one({"info_id" : url['info']})['info_num'] #각각의 url별 정해진 info_num 을 가져온다.
		for post in each_posts:
			db.posts.update_one(
				{'_id': post['_id']},
				{"$set": {"info_num": each_info_num}}
			)
		print(info," 완료!!")

#리토크나이저 함수
def retokenizer(db):
	for url in List:
		each_url_posts = list(db.posts.find(
			{"info":url["info"]})
			)
		for post_one in each_url_posts:
			if post_one["title"][-3:] == "..." and post_one["post"].startswith(post_one["title"][:-3]):
				post_one["title_token"] = post_one["post"][:20].split(" ")
			else:
				post_one["title_token"] = post_one["title"].split(" ")
			if post_one["post"].startswith(post_one["title"][:-3]):
				post_one["token"] = TK.get_tk(post_one["post"].lower())
			else:
				post_one["token"] = TK.get_tk(post_one["title"].lower() + post_one["post"].lower())
			post_one["token"] = list(url['title_tag'] + post_one["token"])

			if 'token' in post_one:
				topic_str = post_one["token"]
			else:
				topic_str = []
			post_one["topic_vector"] = FT.doc2vec(topic_str).tolist()
			db.posts.update_one(
				{'_id':post_one['_id']},
				{"$set":{

					"title_token":post_one["title_token"],
					"token":post_one["token"],
					"topic_vector":post_one["topic_vector"]
					}
				}
			)

if __name__ == '__main__':
	database = connect_db()
	db = database[1]
	client = database[0]

	#리토크나이저 로컬 테스트용
	retokenizer(db)

	#셀레니움 테스트
	# test_selenium()
	
	
	#info num, info 정상매치 함수
	# matching_info_num(db)

	#각 url별 게시글 개수
	# get_post_url(db)

	#signus db collection 전체 삭제
	# drop_all_collection(db)

	# posts 데이터 초기화
	# drop_db_collection(db)

	# posts 데이터 삭제
	# remove_db_posts(db)

	# date collection insert
	# insert_db_date(db)

	# date db초기화
	# init_db_date(db)
	
	# 세종대 관련 url 삭제 함수
	# getPostCnt(db)
	
	# 교내, 교외 공모전 데이터 함수
	# start_time = timeit.default_timer()
	# insideCampus, outsideCampus = getData(db, 300)
	# terminate_time = timeit.default_timer()

	# print("\n")
	# print("test case 10개")    
	# print("<<교내 공모전 데이터 개수:",len(insideCampus),">>")
	# print("------------------------------------------")
	
	# for i in range(0,100):
	#     print(i+1,"번째 리스트의 타이틀 :",insideCampus[i]["title"])
	#     print(i+1,"번째 리스트의 태그 :",insideCampus[i]["tag"])
	#     print(i+1,"번째 리스트의 info :",insideCampus[i]["info"])
	#     print(i+1,"번째 리스트의 게시글 작성 날짜 :",insideCampus[i]["date"])
	#     print("------------------------------------------")
	# print("\n")    
	
	# print("test case 10개")    
	# print("<<교외 공모전 데이터 개수:",len(outsideCampus),">>")
	# print("------------------------------------------")
	
	# for i in range(0,10):
	#     print(i+1,"번째 리스트의 타이틀 :",outsideCampus[i]["title"])
	#     print(i+1,"번째 리스트의 태그 :",outsideCampus[i]["tag"])
	#     print(i+1,"번째 리스트의 info :",outsideCampus[i]["info"])
	#     print(i+1,"번째 리스트의 게시글 작성 날짜 :",outsideCampus[i]["date"])
	#     print("------------------------------------------")

	# print("\n교내 공모전 개수 + 교외 공모전 개수 =",len(insideCampus)," +",len(outsideCampus)," =",len(insideCampus)+len(outsideCampus))

	# print("\n------------------------------------------")
	# print("\n실행 속도 :",(terminate_time - start_time),"초")
	# print("\n------------------------------------------")