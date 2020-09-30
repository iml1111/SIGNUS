from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from modules.crawler.login import everytime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.crawler.etc.driver_agent import chromedriver
from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
def Parsing_list_url(URL, page_url, driver):
	List = []
	domain = Domain_check(URL['url'])

	#만약 driver이 켜져있으면 끄고, 없으면 그냥 진행
	try:
		driver.quit()
	except:
		pass

	driver = chromedriver()
	driver = everytime.login(driver)

	#에브리타임 게시판이 사라졌을 경우 대비
	try:
		driver.get(page_url)
		driver.implicitly_wait(3)
	except:
		data = (driver, List)
		return data

	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.article")))
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')
	
	posts = bs.find("div", {"class": 'wrap articles'}).findAll("article")
	if len(posts) == 1:		#게시물이 아무것도 없는 경우
		pass
	else:
		for post in posts:
			url = post.find("a")['href']
			url = domain + url
			List.append(url)

	data = (driver, List)

	return data



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(driver, post_url, URL):
	return_data = []
	post_data = {}
	domain = Domain_check(URL['url'])
	

	driver.get(post_url)

	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "time.large"))) #time.large를 발견하면 에이작스 로딩이 완료됬다는 가정
	except:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "time.large")))
		except:
			return return_data
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')
	
	if URL['info'].split("_")[2] == 'free' or URL['info'].split("_")[2] == 'notice' or URL['info'].split("_")[2] == 'jobinfo' or URL['info'].split("_")[2] == 'promotion'\
or URL['info'].split("_")[2] == 'club' or URL['info'].split("_")[2] == 'trade':
		title = bs.find("h2", {"class": "large"}).text.strip()
	else:
		title = "!@#$soojle-notitle" + bs.find("p", {'class': "large"}).get_text(" ", strip = True)
		if len(title) >= 300:
			title = title[:299]

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
		

	post_data['title'] = title.upper()
	post_data['author'] = author.upper()
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