
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
from modules.crawler.list.date_cut import date_cut_dict_before
import datetime
from modules.crawler.dbs.mongo.db_connect import *
import pymongo
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
    # INFO_LIST=["thinkgood_info","campuspick_activity","campuspick_contest","campuspick_language",\
	# 	"campuspick_job","campuspick_certificate","campuspick_study","campuspick_club","everytime_all",\
	# 		"detizen_contest","detizen_activity","jobkoreatip_tip","jobkorea_job","jobkorea_public",\
	# 			"rndjob_job","indeed_job","infor_notice","external_notice","review_data","addcampus_board",\
	# 				"20lab_column","20lab_infographics","20lab_announcement","20lab_data","20lab_report",\
	# 					"vms_volunteer","naver_news","campuspick_parttime","univ20_main","kosaf_info"]
	# for item in INFO_LIST:
	# 	db.posts.remove({"info":item})
	db.posts.drop()
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

if __name__ == '__main__':
	database = connect_db()
	db = database[1]
	client = database[0]

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