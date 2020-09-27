from bs4 import BeautifulSoup
import datetime
from modules.crawler.login import everytime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from modules.crawler.etc.driver_agent import chromedriver
from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
def Parsing_list_url(URL, page_url, driver):
	List = []

	#만약 driver이 켜져있으면 끄고, 없으면 그냥 진행
	try:
		driver.quit()
	except:
		pass

	driver = chromedriver()
	driver.get(page_url)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchForm")))
	time.sleep(2)
	
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')

	try:
		posts = bs.find("div",{"class":"table_wrap"}).find("tbody").find_all("tr")
	except:
		try:
			posts = bs.find("div",{"class":"table_wrap"}).find("tbody").find_all("tr")
		except:
			data = (driver, List)
			return data
	try:
		for post in posts:
			url = (post.find("a")["href"]).split("'")[1]
			url = "https://www.youthcenter.go.kr/board/boardDetail.do?bbsNo=3&ntceStno=" + url + "&pageUrl=board%2Fboard&orderBy=REG_DTM&orderMode=DESC"
			List.append(url)
	except:
		List = []

	data = (driver, List)

	return data



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(driver, post_url, URL):
	return_data = []
	post_data = {}
	
	try:
		driver.get(post_url)

		time.sleep(0.5) #마땅한 기다릴 요소가 없기에 time.sleep(0.5)를 해준다. 네트워크 및 컴퓨터 사양에 따라 ~3까지 증감시킬 것.
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		
		title = bs.find("div",{"class":"tit-box"}).find("h3").get_text(" ", strip = True)
		date = bs.find("div",{"class":"tit-box"}).find("span").get_text(" ", strip = True)
		date = date + " 00:00:00"
		date = str(datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S"))
		post = bs.find("div", {"class": "view-txt"}).get_text(" ", strip = True)
		post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
		if bs.find("meta", {"property": "og:image"}) is None:
			img = 7
		else:
			try:
				img = bs.find("meta", {"property": "og:image"}).get("content")	#게시글의 첫번째 이미지를 가져옴.
				if 1000 <= len(img):
					img = 7
				else:
					if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
						pass 
					elif img.startswith("//"):
						img = "http:" + img
					else:
						pass
			except:
				img = 7
		if img != 7:
			if img_size(img):
				pass
			else:
				img = 7
	except:
		driver.get(post_url)

		time.sleep(0.5) #마땅한 기다릴 요소가 없기에 time.sleep(0.5)를 해준다. 네트워크 및 컴퓨터 사양에 따라 ~3까지 증감시킬 것.
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		
		title = bs.find("div",{"class":"tit-box"}).find("h3").get_text(" ", strip = True)
		date = bs.find("div",{"class":"tit-box"}).find("span").get_text(" ", strip = True)
		date = date + " 00:00:00"
		date = str(datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S"))
		post = bs.find("div", {"class": "view-txt"}).get_text(" ", strip = True)
		post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
		if bs.find("meta", {"property": "og:image"}) is None:
			img = 7
		else:
			try:
				img = bs.find("meta", {"property": "og:image"}).get("content")	#게시글의 첫번째 이미지를 가져옴.
				if 1000 <= len(img):
					img = 7
				else:
					if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
						pass 
					elif img.startswith("//"):
						img = "http:" + img
					else:
						pass
			except:
				img = 7
		if img != 7:
			if img_size(img):
				pass
			else:
				img = 7
		

	post_data['title'] = title.upper()
	post_data['author'] = ''
	post_data['date'] = date
	post_data['post'] = post.lower()
	post_data['img'] = img
	post_data['url'] = post_url

	return_data.append(post_data)
	return_data.append(title)
	return_data.append(date)
	return return_data



#url을 받으면 Page를 변환시켜서, 변환된 url 반환
def Change_page(url, page):
	url_done = url + str(page)

	return url_done


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출
	# domain = https://www.example.com
	return domain