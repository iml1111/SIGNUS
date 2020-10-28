from bs4 import BeautifulSoup
import datetime
from modules.crawler.login import everytime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from modules.crawler.dbs.mongo.db_manager import db_manager

from modules.crawler.etc.driver_agent import chromedriver
from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

from modules.crawler.list.date_cut import date_cut


def init(URL, end_data, db):
	url = URL['url']
	driver = chromedriver()
	driver.get(url)
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it('bbsFrm'))

	page = 1 #n번째 페이지
	cnt = 0 #시작 페이지는 메소드 호출 x, 2번 페이지부터 js 함수 호출 위한 조건변수

	while 1:
		post_data_prepare = []
		element = driver.find_element_by_xpath('/html/body/div/div[3]')
		method = "sendPage('pageForm'," + str(page) + ");" #다음 페이지 로드할 메소드
		if cnt != 0:
			try:
				driver.execute_script(method,element) # 다음 페이지 로드
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pagination")))
			except :
				print("페이지가 더이상 존재하지 않습니다.")
				break
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')

		data = list(bs.find("tbody").findAll("tr"))
		posts = []
		for item in data:
			link = item.find("td",{"class":"subject"}).find("a")["href"]
			posts.append(link)

		page = page + 1	
		cnt = cnt + 1
		
		post_data_prepare = get_data(posts, URL, end_data)
		added_post_cnt = db_manager(URL, post_data_prepare, db) 
		print("Added Post Count : ", added_post_cnt)
	driver.close()

# 페이지 하나의 각각의 게시글들 들어가서 데이터 뽑아오는 메소드
def get_data(posts, URL, end_data):
	driver = chromedriver()
	return_data = []
	for post in posts:
		post_data = {}
		post_url = Domain_check(URL['url']) + "/bbs/" + post
		driver.get(post_url)
		post_source = driver.page_source
		bs_post = BeautifulSoup(post_source,'html.parser')
		title = bs_post.find("td",{"class":"subject-value"}).get_text(" ",strip = True)
		post_content = bs_post.find("td",{"class":"content"}).get_text(" ",strip = True)
		date = bs_post.find("td",{"class":"date"}).get_text(" ",strip = True).split("작성일")
		date = date[0] + " 00:00:00"
		date = str(datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S"))

		post_data['title'] = title.upper()
		post_data['author'] = ''
		post_data['date'] = date
		post_data['post'] = post_content.lower()
		post_data['img'] = 7
		post_data['url'] = post_url
		print(date, "::::", title)

		if str(date) <= end_data:
			continue
		else:
			return_data.append(post_data)
	driver.close()
	return return_data

	

def Change_page(url, page):
	return url

def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출
	return domain