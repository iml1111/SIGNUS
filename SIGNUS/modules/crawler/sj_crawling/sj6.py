import datetime

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut_dict
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

#게시판 n페이지를 받으면, 그 페이지의 포스트 url 리스트 반환
def Parsing_list_url(URL, bs):
	List = []
	domain = Domain_check(URL['url'])
	posts = bs.find("tbody").findAll("tr")

	for post in posts:
		if post.find("a") is None:
			continue
		else:
			post_url = post.find("a")["href"]
			post_url = post_url[2:]
		#post_url 이 외부링크면 바로 List 추가, 아니면 domain 추가한 후 List 추가
		if post_url.startswith("http://"):
			List.append(post_url)
		else:
			post_url = domain + post_url
			List.append(post_url)
	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	return_data = []
	post_data = {}

	tds = bs.findAll("span", {"class": "boardTd"})

	title = tds[0].get_text(" ", strip = True)
	author = tds[1].text.strip()
	if author.find("관리자") != -1:
		author = "0"
	date = tds[2].text.strip()
	date = str(datetime.datetime.strptime(date, "%Y/%m/%d %H:%M:%S"))
	post = bs.find("div", {"class": "xed"}).get_text(" ", strip = True)
	post = post_wash(post)		#post 의 공백을 전부 제거하기 위함

	post_data['title'] = title.upper()
	post_data['author'] = author.upper()
	post_data['date'] = date
	post_data['post'] = post.lower()
	post_data['img'] = 1	#세종대 관련글이므로 1을 넣어준다.
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