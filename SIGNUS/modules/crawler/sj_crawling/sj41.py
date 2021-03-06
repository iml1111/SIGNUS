from bs4 import BeautifulSoup
import datetime

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut_dict
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
def Parsing_list_url(URL, bs):
	List = []

	#리스트 반환
	posts = bs.find("table", {"class": 'bbs_ltype interview tbl30'}).findAll("tr")
	for post in posts:
		url = post.find("td",{"class":"thum"}).find("a")['href']
		List.append(url)
	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	try:
		return_data = []
		post_data = {}
		domain = Domain_check(URL['url'])

		title = bs.find("h3", {"class": "hd"}).find("a").get_text(" ", strip = True) + " 채용설명회 후기"
		author = ""
		date = bs.find("dl", {"class": "explainInfoBx"}).find("dd").text.strip()
		date = date + " 00:00:00"
		date = str(datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S"))
		post = bs.find("div",{"class":"explainCtWrap"}).find("p", {"class": "tx"}).get_text(" ", strip = True)
		post = post_wash(post)
		if bs.find("div", {"class": "img"}).find("img") is None:
			img = 1
		else:
			img = bs.find("div", {"class": "img"}).find("img")['src']		#게시글의 첫번째 이미지를 가져옴.
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
		post_data['author'] = ''
		post_data['date'] = date
		post_data['post'] = post.lower()
		post_data['img'] = img
		post_data['url'] = post_url

		return_data.append(post_data)
		return_data.append(title)
		return_data.append(date)
		return return_data
	except:
		return None



#url을 받으면 Page를 변환시켜서, 변환된 url 반환
def Change_page(url, page):
	url_done = url + str(page)

	return url_done


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2] + "/" + url.split('/')[3]		#도메인 url 추출

	return domain