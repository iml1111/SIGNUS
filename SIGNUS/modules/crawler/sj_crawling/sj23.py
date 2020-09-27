from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from modules.crawler.login import everytime
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

	#만약 driver이 켜져있으면 끄고, 없으면 그냥 진행
	try:
		driver.quit()
	except:
		pass

	driver = chromedriver()

	List.append(page_url)
	

	data = (driver, List)

	return data



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(driver, post_url, URL, recent_post):
	post_data_prepare = []
	domain = Domain_check(URL['url'])
	end_date = date_cut(URL['info'])
	now_num = 0
	repeat_num = 0

	driver.get(post_url)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.header"))) #div.header을 발견하면 에이작스 로딩이 완료됬다는 가정

	#비교를 하기위해서 make
	last_posts = [0]
	while 1:
		driver.get(post_url)
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.header"))) #div.header을 발견하면 에이작스 로딩이 완료됬다는 가정

		for i in range(repeat_num):
			driver.find_element_by_tag_name("body").send_keys(Keys.END)
			time.sleep(0.2)

		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')

		posts = bs.find("div", {"id": 'items'}).findAll("a", {"class": "item"})
		#더이상 내릴 수 없으면 break
		if len(last_posts) == len(posts):
			break
		else:
			last_posts = posts

		for post in posts[now_num:]:
			post_data = {}
			url = post['href']
			url = domain + url

			driver.get(url)
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.group"))) #a.item을 발견하면 에이작스 로딩이 완료됬다는 가정
			html_post = driver.page_source
			bs_post = BeautifulSoup(html_post, 'html.parser')

			title = bs_post.find("div", {"class": "group"}).get_text(" ", strip = True)
			author = bs_post.find("span", {"class": "text"}).text.strip()
			date = bs_post.find("time").text.strip()
			date = everytime_time(date)
			if bs_post.find("p", {"class": "comment"}) is None:
				
				if bs_post.find("p", {"class": "soldout"}) is not None:
					phrase = bs_post.find("p", {"class": "soldout"}).get_text(" ", strip = True)
				else:
					phrase_vocas = bs_post.findAll("span", {"class": "text"})
					phrase = phrase_vocas[1].get_text(" ", strip = True)
				phrase = post_wash(phrase)
			else:
				phrase = bs_post.find("p", {"class": "comment"}).get_text(" ", strip = True)
				phrase = post_wash(phrase)
			if bs_post.find("div", {"class": "image"}) is None:
				img = 5
			else:
				try:
					img = bs_post.find("div", {"class": 'image'})['style']
					img = img.split('"')[1]
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
			if img != 5:
				if img_size(img):
					pass
				else:
					img = 5

			post_data['title'] = title.upper()
			post_data['author'] = author.upper()
			post_data['date'] = date
			post_data['post'] = phrase.lower()
			post_data['img'] = img
			post_data['url'] = url

			print(date, "::::", title)

			if (date < end_date) or (title.upper() == recent_post):
				break
			else:
				if bs_post.find("p", {"class": "soldout"}) is not None:
					print("\nNot Append :::: SoldOut!\n")
					pass
				else:
					post_data_prepare.append(post_data)

		now_num = len(posts)
		repeat_num += 1
		if (date <= end_date) or (title.upper() == recent_post):
			break
	if len(post_data_prepare) == 0:
		recent_post = None
	else:
		recent_post = post_data_prepare[0]['title']
	data = (post_data_prepare, recent_post)
	return data



#url을 받으면 url 그대로 반환해준다. => Page number이 필요하지 않는 url
def Change_page(url, page):

	return url


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain
	

def everytime_time(date):
	year = date.split("년")[0]
	month = date.split("년")[1]
	month = month.split("월")[0]
	month = month[1:]
	if int(month) < 10:
		month = "0"+month
	day = date.split("일")[0]
	day = day.split("월")[1]
	day = day[1:]
	if int(day) <10:
		day = "0"+day
	output = year + "-" + month + "-" + day + " 00:00:00"

	return output