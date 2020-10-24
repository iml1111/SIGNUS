from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from modules.crawler.login import campuspick
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
	post_driver = chromedriver()	# 포스트 페이지를 위한 드라이버
	driver.get(post_url)
	if (URL['info'].split("_")[2] == "campustown"):
		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.card")))
		driver.find_element_by_xpath('//*[@id="ct"]/div[5]/div/div[1]/div/button[2]').click()
		
	else:
		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.area_text"))) #div.header을 발견하면 에이작스 로딩이 완료됬다는 가정
	last_posts = [0]
	while 1:
		if (now_num > 0) and (now_num % 100 == 0):
			print("post_driver를 재시작 합니다.")
			post_driver.close()
			post_driver = chromedriver()	# 포스트 페이지를 위한 드라이버
			post_driver = campuspick.login(post_driver)
		
		driver.find_element_by_tag_name("body").send_keys(Keys.END)
		time.sleep(1)

		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')

		posts = bs.find("div", {"class": 'wrap_postlist'}).findAll("div", {"class": "item"})
		#더이상 내릴 수 없으면 break
		if len(last_posts) == len(posts):
			break
		else:
			last_posts = posts

		for post in posts[now_num:]:
			try:
				post_data = {}
				url = post.find("a", {"class": "link"})['href']
				url = domain + url

				try:
					post_driver.get(url)
				except:
					if len(post_data_prepare) == 0:
						recent_post = None
					else:
						recent_post = post_data_prepare[0]['title']
					data = (post_data_prepare, recent_post)
					return data
				try:
					WebDriverWait(post_driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.txt_area"))) #a.item을 발견하면 에이작스 로딩이 완료됬다는 가정
				except Exception as e:
					print(e)
				except:
					if len(post_data_prepare) == 0:
						recent_post = None
					else:
						recent_post = post_data_prepare[0]['title']
					data = (post_data_prepare, recent_post)
					return data
				html_post = post_driver.page_source
				bs_post = BeautifulSoup(html_post, 'html.parser')

				if (URL['info'].split("_")[2] == "campustown"):
					title = bs_post.find("h3", {"class": "tit_h3"}).get_text(" ", strip = True)
				else:
					if bs_post.find("div", {"class": "se-module se-module-text se-title-text"}) == None:
						title = bs_post.find("h3", {"class": "tit_h3"}).get_text(" ", strip = True)
					else:
						title = bs_post.find("div", {"class": "se-module se-module-text se-title-text"}).find("span").get_text(" ", strip = True)
				if bs_post.find("p", {"class": "blog_date"}) == None:
					date = bs_post.find("p", {"class": "se_date"}).get_text(" ", strip = True)
				else:
					date = bs_post.find("p", {"class": "blog_date"}).get_text(" ", strip = True)
				if date.find("시간") != -1 or date.find("분") != -1 or date.find("초") != -1:
					now = datetime.datetime.now().strftime("%Y-%m-%d")
					date = now + " 00:00:00"
					date = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
				else:
					date = date + ":00"
					date = str(datetime.datetime.strptime(date, "%Y. %m. %d. %H:%M:%S"))
				if (URL['info'].split("_")[2] == "campustown"):
					phrase = bs_post.find("div", {'class': "post_ct"}).get_text(" ", strip = True)
				else:
					phrase = bs_post.find("div", {'class': "se-main-container"}).get_text(" ", strip = True)
				phrase = post_wash(phrase)		#post 의 공백을 전부 제거하기 위함
				if (URL['info'].split("_")[2] == "campustown"):
					if bs_post.find("div", {'class': "post_ct"}).find("img", {"id": "img_1"}) is None:
						img = 3
					else:
						img = bs_post.find("div", {"class": "post_ct"}).find("img", {"id": "img_1"})['src']		#게시글의 첫번째 이미지를 가져옴.
						if 1000 <= len(img):
							img = 3
						else:
							if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
								pass
							elif img.startswith("//"):
								img = "http:" + img
							else:
								img = domain + img
				else:
					if bs_post.find("div", {"class": "se-main-container"}).find("img", {"id": "img_2"}) is None:
						img = 3
					else:
						img = bs_post.find("div", {"class": "se-main-container"}).find("img", {"id": "img_2"})['src']		#게시글의 첫번째 이미지를 가져옴.
						if 1000 <= len(img):
							img = 3
						else:
							if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
								pass
							elif img.startswith("//"):
								img = "http:" + img
							else:
								img = domain + img
				if img != 3:
					if img_size(img):
						pass
					else:
						img = 3	

				post_data['title'] = title.upper()
				post_data['author'] = "0"
				post_data['date'] = date
				post_data['post'] = phrase.lower()
				post_data['img'] = img
				post_data['url'] = "https://" + url[10:]	# 'm'떼어버리는 작업

				print(date, "::::", title)

				if (date < end_date) or (title.upper() == recent_post):
					break
				else:
					post_data_prepare.append(post_data)
			except:
				continue

		now_num = len(posts)
		if (date <= end_date) or (title.upper() == recent_post):
			break
	if len(post_data_prepare) == 0:
		recent_post = None
	else:
		recent_post = post_data_prepare[0]['title']
	data = (post_data_prepare, recent_post)
	post_driver.close()
	return data

#url을 받으면 url 그대로 반환해준다. => Page number이 필요하지 않는 url
def Change_page(url, page):
	return url


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출
	return domain