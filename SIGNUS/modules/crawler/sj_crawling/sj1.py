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

		#post_url 이 외부링크면 바로 List 추가, 아니면 domain 추가한 후 List 추가
		if post_url.startswith("http://"):
			List.append(post_url)
		else:
			if URL['info'] == "sj1_main_founded":
				post_url = post_url.split("swc")[0] + "swc&current" + post_url.split("swc")[1][2:]
				post_url = domain + "/bbs/" + post_url
			else:
				post_url = domain + post_url
			List.append(post_url)
	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	return_data = []
	post_data = {}
	domain = Domain_check(URL['url'])

	title = bs.find("td", {"class": "subject-value"}).get_text(" ", strip = True)
	author = bs.find("td", {"class": "writer"}).text.strip()
	if author.find("관리자") != -1:
		author = "0"
	date = bs.find("td", {"class": "date"}).text
	if URL['info'] == "sj1_main_founded":
		date = date + " 12:00:00"
	date = str(datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S"))
	post = bs.find("tbody").find("div").get_text(" ", strip = True)
	post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
	if bs.find("tbody").find("tr").find("img"):
		img = bs.find("tbody").find("tr").find("img")["src"]
		if 1000 <= len(img):
			img = 1
		else:
			if img.startswith("http://") or img.startswith("https://") or img.startswith("data:"):		# img가 내부링크인지 외부 링크인지 판단.
				pass
			elif img.startswith("//"):
				img = "http:" + img
			else:
				img = domain + img
	else:
		img = 1
	if img != 1:
		if img_size(img):
			pass
		else:
			img = 1
			
	post_url_a = post_url.split("&viewNum=")[0]
	post_url_b = post_url.split("&viewNum=")[1]
	while post_url_b[0] != '&':
		post_url_b = post_url_b[1:]
	post_url = post_url_a+post_url_b

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
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain