from bs4 import BeautifulSoup
import datetime
from modules.crawler.etc.url_parser import URLparser

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
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchMove")))
	time.sleep(2)
	
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')

	try:
		posts = bs.find("ul",{"id":"searchMove"}).findAll('li')
	except:
		try:
			posts = bs.find("ul",{"id":"searchMove"}).findAll('li')
		except:
			data = (driver, List)
			return data
	try:
		for post in posts:
			parse_url = ((post.find("a")["onclick"]).split(","))[0]
			url = (parse_url.split('('))[1]
			url = 'https://youth.seoul.go.kr/site/youthzone/youth/politics/program/detail/' + url
			List.append(url)
	except:
		List = []

	data = (driver, List)
	return data



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(driver, post_url, URL):
	return_data = []
	post_data = {}
	

	driver_page = URLparser(post_url)
	bs = BeautifulSoup(driver_page, 'html.parser')

	except_check = list(bs.find("div",{"class":"srv_rt"}).find("ul").findAll("li"))	
	current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	end_date = ''
	# 마감날짜가 현재날짜보다 지난 포스트인 경우 가져오지 않기 위해 먼저 예외처리
	dead_line = str(except_check[3].get_text()).strip() # 사이트내 진행일정 부분
	# ex 1) 2000. 12. 31 (진행시간 ~~) , 94~98자
	# ex 2) 2000. 12. 31
	# ex 3) 상시모집
	# ex 4) 2000. 12. 31 ~ 2001. 1. 31, 92~96자
	# ex 5) 2000. 12. 31 ~ 2001. 1. 31 (진행시간 ~~)
	if dead_line == '상시모집':
		dead_line = ''
	elif len(dead_line) > 12: # ex 4), ex 1), ex 5)
		if '진행시간' in dead_line: # ex 1)
			dead_line = (dead_line.split('(진행시간')[0]).strip()
			if len(dead_line) > 12: #ex 5)
				dead_line = (dead_line.split('~')[0]).strip()
		else: #ex 4)
			dead_line = (dead_line.split('~')[1]).strip()
	else: #ex 2)
		dead_line = dead_line
	
	if dead_line != '':
		dead_line = dead_line + " 00:00:00"
		dead_line = str(datetime.datetime.strptime(dead_line, "%Y. %m. %d %H:%M:%S"))
		if dead_line < current_time: #진행기간이 현재시간보다 지난 경우 예외처리
			return None
		else:
			end_date = dead_line
	
	title = bs.find("div",{"class":"tits"}).find("p").get_text(" ", strip = True)

	not_splited_date = str(except_check[1].get_text()).strip() # 사이트내 신청기간 부분
	date = current_time
	# ex 1) 상시모집
	# ex 2) 2000. 12. 31 ~ 2001. 1. 31
	if not_splited_date != '상시모집': # ex 2)
		end_date = (not_splited_date.split('~')[1]).strip() + " 00:00:00"
		end_date = str(datetime.datetime.strptime(end_date, "%Y. %m. %d %H:%M:%S"))
	if end_date < current_time: # 신청기간이 마감된 경우 예외처리
		return None

	post = bs.find("div", {"class": "etc_box"}).get_text(" ", strip = True)
	post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
	if bs.find("div", {"class": "etc_box"}).find('img') is None:
		img = 7
	else:
		try:
			img = bs.find("div", {"class": "etc_box"}).find('img')['src']	#게시글의 첫번째 이미지를 가져옴.
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
	if end_date != '':
		post_data['title'] = title.upper()
		post_data['author'] = ''
		post_data['date'] = date
		post_data['post'] = post.lower()
		post_data['img'] = img
		post_data['url'] = post_url
		post_data['end_date'] = end_date
	else :
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