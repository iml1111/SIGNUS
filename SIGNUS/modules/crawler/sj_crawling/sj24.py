import datetime

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut_dict
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

#게시판 n페이지를 받으면, 그 페이지의 포스트 url 리스트 반환
def Parsing_list_url(URL, bs):
	List = []
	domain = Domain_check(URL['url'])
	try:
		posts = bs.find("div", {"id": "result-list"}).findAll("div", {"class": "media"})
	except:
		return List
	if len(posts) == 0:
		pass
	else:
		for post in posts:
			url = post.find("a")['href']
			url = domain + url
			List.append(url)

	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	return_data = []
	post_data = {}
	domain = Domain_check(URL['url'])

	title = bs.find("h1", {"class": "title-news"}).get_text(" ", strip = True)
	author = bs.find("div", {"class": "info-news"}).find("span", {"class": "category"}).text.strip()
	if author.find("관리자") != -1:
		author = "0"
	date = bs.find("div", {"class": "info-news"}).find("span", {"class": "date-created"}).text.strip()
	date = date + " 00:00:00"
	date = str(datetime.datetime.strptime(date, "%Y년 %m월 %d일 %H:%M:%S"))
	post = bs.find("div", {"class": "main-news"}).get_text(" ", strip = True)
	post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
	if bs.find("div", {"class": "main-news"}).find("img") is None:
		img = 6
	else:
		try:
			img = bs.find("div", {"class": "main-news"}).find("img")['src']		#게시글의 첫번째 이미지를 가져옴.
			if 1000 <= len(img):
				img = 6
			else:
				if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
					pass
				elif img.startswith("//"):
					img = "http:" + img
				else:
					img = domain + img
		except:
			img = 6
	if img != 6:
		if img_size(img):
			pass
		else:
			img = 6

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


#입력된 url의 도메인 url 반환 :::: sj10 에 한해서 /bbs/ 까지 뽑힘
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain