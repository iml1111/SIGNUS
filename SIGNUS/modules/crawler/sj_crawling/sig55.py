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
	
	#캠퍼스픽 로그인함수
	driver = campuspick.login(driver)
	List.append(page_url)

	data = (driver, List)
	return data



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(driver, post_url, URL, recent_post):
	post_data_prepare = []
	domain = Domain_check(URL['url'])
	end_date = date_cut(URL['info'])
	now_num = 0
	end_dday = 0
	driver.get(post_url)
	post_driver = chromedriver()
	post_driver = campuspick.login(post_driver)
	last_posts = [0]
	flag = 0 # 마감 게시물 연속으로 인한 종료시 값 전달 변수

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
		
		posts = bs.find("div", {"class": 'list'}).findAll("a", {"class": "top"})
		#더이상 내릴 수 없으면 break
		if len(last_posts) == len(posts):
			break
		else:
			last_posts = posts
		
		for post in posts[now_num:]:
			if end_dday == 20: #마감 게시물이 연속으로 20개가 보이면 종료
				flag = 1
				break
			try:
				post_data = {}
				url = post['href']
				url = domain + url
				try:
					post_driver.get(url)
					#driver.get(url)
				except:
					if len(post_data_prepare) == 0:
						recent_post = None
					else:
						recent_post = post_data_prepare[0]['title']
					data = (post_data_prepare, recent_post)
					return data
				try:
					WebDriverWait(post_driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.company"))) #a.item을 발견하면 에이작스 로딩이 완료됬다는 가정
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
				
				title = bs_post.find("p",{"class":"company"}).get_text(" ", strip = True) + bs_post.find("div",{"class":"content figure"}).find("h1").get_text(" ",strip = True)
				now = datetime.datetime.now()
				date =  now.strftime("%Y-%m-%d %H:%M:%S")
				post_content = bs_post.find("div", {'id': "container"}).findAll("div",{"class":"section"})
				post_content = post_content[0].get_text(" ", strip = True)+post_content[1].get_text(" ",strip = True)
				post_content = post_wash(post_content)		#post 의 공백을 전부 제거하기 위함

				dead_line = str((bs_post.find("p",{"class":"dday"}).get_text(" ",strip=True)))
				if dead_line == "마감":
					end_dday = end_dday + 1
				else:
					end_dday = 0
					post_data['title'] = title.upper()
					post_data['author'] = ''
					post_data['date'] = date
					post_data['post'] = post_content.lower()
					post_data['img'] = 7
					post_data['url'] = url
					print(date, "::::", title)
					if (date < end_date) or (title.upper() == recent_post):
						break
					else:
						post_data_prepare.append(post_data)
			except:
				continue
		
		now_num = len(posts)
		print("now_num : ", now_num)
		if (date <= end_date) or (title.upper() == recent_post) or (flag == 1):
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