from bs4 import BeautifulSoup
from modules.crawler.etc.url_parser import URLparser
from modules.crawler.dbs.mongo.db_manager import db_manager
from selenium import webdriver
import datetime
from modules.crawler.login import everytime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.crawler.etc.error_handler import error_handler
from modules.crawler.etc.error_handler import continue_handler
from modules.crawler.etc.error_handler import error_logging
import re

from modules.crawler.etc.driver_agent import chromedriver
from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

SJ34_DELETE_TAGS = ["갤러리", "게시판"]

#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
def Parsing_list_url(main_url, page_url, driver, db):
	List = []
	domain = main_url

	driver.get(page_url)

	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.comments")))
	except:
		return List
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')
	
	#posts = bs.find("div", {"class": 'wrap articles'}).findAll("article")
	posts = bs.findAll("article")
	if len(posts) == 1:		#게시물이 아무것도 없는 경우
		pass
	else:
		for post in posts:
			url = post.find("a")['href']
			url = domain + url
			List.append(url)
	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(driver, post_url, URL, board_tag, db):
	return_data = []
	post_data = {}
	domain = Domain_check(URL['url'])
	
	try:
		driver.get(post_url)
	except:
		try:
			time.sleep(3)
			driver.get(post_url)
		except:
			return "error"


	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "time.large"))) #time.large를 발견하면 에이작스 로딩이 완료됬다는 가정
	except:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "time.large")))
		except Exception as e:
			error_handler(e, URL, post_url, db)
			return "error"

	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')
	if bs.find("h2", {"class": "large"}) != None:
		title = bs.find("h2", {"class": "large"}).get_text(" ", strip = True)
	else:
		title = "0"
	author = "0"
	date = bs.find("time").text.strip()
	date = everytime_time(date)
	post = bs.find("p", {'class': "large"}).get_text(" ", strip = True)
	post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
	if bs.find("figure", {"class": "attach"}) is not None:
		try:
			img = bs.find("figure", {"class": "attach"}).find("img")['src']		#게시글의 첫번째 이미지를 가져옴.
			if 1000 <= len(img):
				img = 5
			else:
				if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
					pass
				elif img.startswith("//"):
					img = "http:" + img
				else:
					img = domain + img
		except:
			img = 5
	else:
		img = 5
	if img != 5:
		if img_size(img):
			pass
		else:
			img = 5
	img = 5

	post_data['title'] = title.upper()
	post_data['author'] = author.upper()
	post_data['date'] = date
	post_data['post'] = post.lower()
	board_tag = re.compile('[^ ㄱ-ㅣ가-힣|a-z]+').sub('', board_tag.lower())
	for remove_tag in SJ34_DELETE_TAGS:
		board_tag = board_tag.replace(remove_tag, "")
	post_data['img'] = img
	post_data['url'] = post_url
	post_data['info'] = URL['info'].split("_")[1] + "_" + board_tag
	if post_data["title"] == "0":
		post_data["title"] = post_data["post"][:30] + "..."

	return_data.append(post_data)
	return_data.append(post_data['title'])
	return_data.append(date)
	return return_data



#url을 받으면 Page를 변환시켜서, 변환된 url 반환
def Change_page(url, page):
	url_done = url + '/p/' + str(page)

	return url_done


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain


#현재 시간 계산하는 함수
def everytime_time(text):
	if text == "방금":																	#방금 형태
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	elif text.find("분 전") != -1:														#n분 전 형태
		text_minutes = text.split("분")[0]
		date = datetime.datetime.now() - datetime.timedelta(minutes = int(text_minutes))
		date = date.strftime("%Y-%m-%d %H:%M:%S")
	elif len(text.split("/")) == 3:														#18/12/31 00:00 형태
		year = text.split("/")[0]
		month = text.split("/")[1]
		day = text.split("/")[2]
		date = "20" + year + "-" + month + "-" + day + ":00"
	else:																				#12/31 00:00 형태
		now_year = datetime.datetime.now().strftime("%Y")
		date = now_year + "/" + text + ":00"
		year = date.split("/")[0]
		month = date.split("/")[1]
		day = date.split("/")[2]
		date = year + "-" + month + "-" + day

	return date

def everytime_all_board(URL, end_date, db):
	main_url = URL['url']
	board_search_url = "https://everytime.kr/community/search?keyword="
	board_search_word = ['게시판', '갤러리']
	board_list = []
	# driver 연결
	try:
		driver = chromedriver()
		driver = everytime.login(driver)
	except Exception as e:
		error_handler(e, URL, main_url, db)
		return
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.article")))
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')
	# 에브리타임 상단 동적 게시판 긁기=============================================================================
	board_group_list = bs.find("div", {"id": "submenu"}).findAll('div', {"class": "group"})
	for board_group in board_group_list:
		try:
			board_li_list = board_group.find("ul").findAll("li")
			for board_li in board_li_list:
				board_li_dic = {}
				board_li_dic['tag'] = board_li.find("a").text
				if board_li.find("a").text.strip() == "더 보기":
					continue
				else:
					board_li_dic['url'] = main_url + board_li.find("a")['href']
				if (board_li_dic['tag'].find("찾기") != -1):
					continue
				board_list.append(board_li_dic)
		except:
			continue
	# 에브리타임 추가 동적 게시판 긁기
	for search_word in board_search_word:
		try:
			board_search_url_done = board_search_url + search_word
			driver.get(board_search_url_done)
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.result")))
			html = driver.page_source
			bs = BeautifulSoup(html, 'html.parser')
			board_a_list = bs.find("div", {"class": "searchresults"}).findAll('a')
			for board_a in board_a_list:
				board_li_dic = {}
				board_li_dic['tag'] = board_a.find("h3").text
				board_li_dic['url'] = main_url + board_a.get('href')
				board_list.append(board_li_dic)
		except:
			continue
	#===========================================================================================================
	# 동적 게시판들 반복문
	for board in board_list:
		page = 1
		page_flag = 0
		board_url = board['url']
		page_url = Change_page(board_url, page)	#현재 페이지 포스트 url 반환
		print("\nTarget : ", URL['info'], " :: ", board['tag'])
		continue_handler(URL['info'] + " :: " + board['tag'], URL, page_url)
		# 페이지 반복문
		while True:
			if page_flag == 50:
				page_flag = 0
				driver.quit()
				time.sleep(3)
				driver = chromedriver()
				driver = everytime.login(driver)
			try:
				print("page_url :::: ", page_url)	#현재 url 출력
				print("Page : ", page)				#현재 페이지 출력
				post_urls = Parsing_list_url(main_url, page_url, driver, db)
				# everytime 고질병 문제 고려, 재시도
				if len(post_urls) == 0:
					time.sleep(2)
					post_urls = Parsing_list_url(main_url, page_url, driver, db)
				post_data_prepare = []
				# 포스트 반복문
				for post_url in post_urls:
					get_post_data = Parsing_post_data(driver, post_url, URL, board['tag'], db)
					if get_post_data == "error":
						break
					title = get_post_data[1]
					date = get_post_data[2]
					print(date, "::::", title)	#현재 크롤링한 포스트의 date, title 출력
					#게시물의 날짜가 end_date 보다 옛날 글이면 continue, 최신 글이면 append
					if str(date) <= end_date:
						continue
					else:
						post_data_prepare.append(get_post_data[0])
				add_cnt = db_manager(URL, post_data_prepare, db)
				print("add_OK : ", add_cnt)	#DB에 저장된 게시글 수 출력
				#DB에 추가된 게시글이 0 이면 break, 아니면 다음페이지
				if add_cnt == 0:
					page_flag = 0
					break
				else:
					page_flag += 1
					page += 1
					page_url = Change_page(board_url, page)
			except Exception as e:
				error_handler(e, URL, page_url, db)
				driver.quit()
				time.sleep(3)
				driver = chromedriver()
				driver = everytime.login(driver)
				break
	#드라이버 연결 해제
	driver.quit()