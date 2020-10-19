from bs4 import BeautifulSoup
import datetime
import urllib3
import time

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut_dict
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size
urllib3.disable_warnings()


#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
def Parsing_list_url(URL, bs):
	List = []
	domain = Domain_check(URL['url'])

	#리스트 반환
	try:
		posts = bs.find("td", {"id": 'resultsCol'}).findAll("h2", {"class": "title"})
	except:
		time.sleep(3)
		posts = bs.find("td", {"id": 'resultsCol'}).findAll("h2", {"class": "title"})

	for post in posts:
		post_url = post.find("a",{"class":"jobtitle"})["href"]
		post_url = domain + post_url
		List.append(post_url)

	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	return_data = []
	post_data = {}
	try:
		title = bs.find("h1",{"class":"icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).get_text(" ", strip = True)
	except Exception as e:
		print(e)
	# try:
	# 	author = bs.find("div", {"class": 'icl-u-lg-mr--sm icl-u-xs-mr--xs'}).text.strip()
	# except:
	# 	author = "Indeed"
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	date = now
	date = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
	try:
		post = bs.find("div", {"id": "jobDescriptionText"}).get_text(" ", strip = True)
	except Exception as e:
		print(e)
	post = post_wash(post)
	img = 1

	post_data['title'] = title.upper()
	# post_data['author'] = author.upper()
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
#한페이지당 16개 * 100페이지 긁음 == 1600개
def Change_page(url, page):
	if page == 1:
		return url
	elif (page * 10 - 10) > 1000:
		page_done = 1000
		url = url + "&start=" + str(page_done)
	else:
		url = url + "&start=" + str(page * 10 -10)
	return url


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain