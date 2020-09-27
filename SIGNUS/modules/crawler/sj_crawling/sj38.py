from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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

	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.aL"))) #time.large를 발견하면 에이작스 로딩이 완료됬다는 가정
	except:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.aL")))
		except:
			return (driver, List)
	html = driver.page_source
	bs = BeautifulSoup(html, 'html.parser')

	posts = bs.find("div", {"class": "tbl_container"}).find("tbody").findAll("tr")
	for post in posts:
		if post.find("th") != None:
			continue
		if len(post.find("td").text) <= 1:
			continue
		url_done = domain + "/" + post.find("td", {"class": "aL"}).find("a")['href']
		List.append(url_done)

	data = (driver, List)
	driver.quit()
	return data



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	return_data = []
	post_data = {}

	title = bs.find("div", {"class": "tbl_container"}).find("th").get_text(" ", strip = True)
	author = bs.find("div", {"class": "tbl_container"}).findAll("tr")[1].findAll("td")[1].text.strip()
	if author.find("관리자") != -1:
		author = "0"
	date = bs.find("div", {"class": "tbl_container"}).findAll("tr")[1].findAll("td")[3].text.strip()
	date = date.replace(" 오전", "")
	date = date.replace(" 오후", "")
	if len(date.split(":")) == 2:
		date = date + ":00"
	date = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
	post = bs.find("div", {"class": "tbl_container"}).findAll("tr")[2].get_text(" ", strip = True)
	post = post_wash(post)
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
	url_done = url.split("page=")[0] + "page=" + str(page) + url.split("page=")[1]
	url_done = url_done.split("viewnum=")[0] + "viewnum=" + str(page * 10 - 10) + url_done.split("viewnum=")[1][1:]

	return url_done


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain