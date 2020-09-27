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
	domain = Domain_check(URL['url'])

	#만약 driver이 켜져있으면 끄고, 없으면 그냥 진행
	try:
		driver.quit()
	except:
		pass

	driver = chromedriver()
	driver.get(page_url)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.li_list")))
	time.sleep(2)
	'''
	for i in range(int(num)):
		driver.find_element_by_xpath('//*[@id="paging"]/li[4]/a').click()
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.li_num")))
	'''
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')

	try:
		posts1 = bs.find("ul", {"class": 'listContent'}).findAll("li")
		posts2 = bs.find("ul", {"class": 'listContent mb20'}).findAll("li")
		posts = posts1 + posts2
	except:
		try:
			posts1 = bs.find("ul", {"class": 'listContent'}).findAll("li")
			posts2 = bs.find("ul", {"class": 'listContent mb20'}).findAll("li")
			posts = posts1 + posts2
		except:
			data = (driver, List)
			return data
	try:
		for post in posts:
			url = post.find("span", {"class": "li_subject li_list2"}).find("a")['onclick']
			url = url.split("'")[1]
			url = domain + url
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
		
		title = bs.find("li", {"class": "vi_subject vi_title"}).get_text(" ", strip = True)
		author = bs.find("span", {"id": "regname"}).text.strip()
		date = bs.find("span", {"id": "regdate"}).text.strip()
		date = date + " 00:00:00"
		date = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
		post = bs.find("li", {"id": "contents"}).get_text(" ", strip = True)
		post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
		img = 1
	except:
		driver.get(post_url)

		time.sleep(0.5) #마땅한 기다릴 요소가 없기에 time.sleep(0.5)를 해준다. 네트워크 및 컴퓨터 사양에 따라 ~3까지 증감시킬 것.
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		
		title = bs.find("li", {"class": "vi_subject vi_title"}).text.strip()
		author = bs.find("span", {"id": "regname"}).text.strip()
		date = bs.find("span", {"id": "regdate"}).text.strip()
		date = date + " 00:00:00"
		date = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
		post = bs.find("li", {"id": "contents"}).text.strip()
		post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
		img = 1
		

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
	#행복기숙사 포스트 url 형식
	domain = "https://happydorm.sejong.ac.kr/sejong/bbs/getBbsWriteView.kmc?&bbs_id=notice&seq="

	return domain