from bs4 import BeautifulSoup
import datetime
from modules.crawler.login import udream

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut_dict
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
def Parsing_list_url(URL, page_url):
	List = []

	#udream 로그인하는 함수
	s = udream.login()

	page = s.get(page_url).text
	bs = BeautifulSoup(page, "lxml")	#html.parser 오류 lxml 로 가져온다.

	#리스트 반환
	posts = bs.findAll("tr", {"onmouseover": "hctrOn(this)"})
	for post in posts:
		num = post.find("a")["onclick"]

		post_num = num.split("'")[1]
		page = URL['post_url'] + post_num
		List.append(page)
	s.close()

	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	return_data = []
	post_data = {}

	title = bs.find("header", {"class": "header b-b bg-light h2"}).find("span").get_text(" ", strip = True)
	author = bs.find("div", {"class": "col-xs-10 lbb"}).text.strip()
	if author.find("관리자") != -1:
		author = "0"
	date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	post = bs.find("section", {"class": "wrapper-lg"}).get_text(" ", strip = True)
	post = post_wash(post)
	img = 1
	end_date = bs.find("span", {"name": "Edate"}).text + " 00:00:00"
	end_date = str(datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S"))

	post_data['title'] = title.upper()
	post_data['author'] = author.upper()
	post_data['date'] = date
	post_data['post'] = post.lower()
	post_data['img'] = img
	post_data['url'] = post_url
	post_data['end_date'] = end_date

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