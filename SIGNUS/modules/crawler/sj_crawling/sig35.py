from bs4 import BeautifulSoup
import datetime

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut_dict
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size


#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
def Parsing_list_url(URL, bs):
	List = []
	domain = Domain_check(URL['url'])

	#리스트 반환
	try:
		posts = bs.find("ul", {"class": 'basic-list page-list'}).findAll("li")
	except:
		return List
	for post in posts:
		target = post.find('a')['href']
		target_start = target.find('?')
		target = target[target_start:]
		page = domain + target
		List.append(page)

	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	return_data = []
	post_data = {}
	domain = URL['url'].split('/')[0] + '//' + URL['url'].split('/')[2]

	title = bs.find("span", {"class": "on"}).get_text(" ", strip = True)
	author = bs.find("table", {"class": "basic-table input-table"}).findAll("tr")[1].find("td").text.strip()
	if author.find("관리자") != -1:
		author = "0"
	date = bs.find("table", {"class": "basic-table input-table"}).findAll("tr")[3].find("td").text.strip()[:23].split('~')[1].strip()
	date = date + " 00:00:00"
	date = str(datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S"))
	post = bs.find("ul", {"class": "summary-info"}).get_text(" ", strip = True)
	post = post_wash(post)
	if bs.find("div", {"class": "poster"}).find("img") is None:
		img = 1
	else:
		img = bs.find("div", {"class": "poster"}).find("img")['src']		#게시글의 첫번째 이미지를 가져옴.
		if 1000 <= len(img):
			img = 1
		else:
			if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
				pass
			elif img.startswith("//"):
				img = "http:" + img
			else:
				img = domain + img
	if img != 1:
		if img_size(img):
			pass
		else:
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
	domain = url.split('/')[0] + '//' + url.split('/')[2] + '/' + url.split('/')[3]	#도메인 url 추출

	return domain