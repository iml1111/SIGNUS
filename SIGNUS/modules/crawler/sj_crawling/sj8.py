from bs4 import BeautifulSoup
from modules.crawler.etc.url_parser import URLparser
import datetime

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size

#게시판 bs_page 을 받으면, 그 페이지의 bs_page 반환
def Parsing_list_url(URL, bs_page):
	List = []

	List.append(bs_page)

	return List



#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, URL):
	post_data_prepare = []
	end_date = date_cut(URL['info'])

	posts = bs.findAll("div", {"class": "item article"})

	for post in posts:
		post_infoes = post.findAll("a")	#td 묶음

		post_data = {}
		try:
			title = post_infoes[0].get_text(" ", strip = True)
			author = post.find("strong").text.strip()
			if author.find("관리자") != -1:
				author = "0"
			date = post.find("span", {"class": "date"})
			date = str(date).split(">")[1]
			date = str(date).split("<")[0]
			date = date + " 00:00:00"
		except:
			title = post_infoes[0].get_text(" ", strip = True)
			try:
				author = post.find("strong").text.strip()
			except:
				author = "0"
			if author.find("관리자") != -1:
				author = "0"
			date = post.find("span", {"class": "date"})
			date = str(date).split(">")[1]
			date = str(date).split("<")[0]
			date = date + " 00:00:00"
		try:
			date = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
		except:
			date = datetime.datetime.now().strftime("%Y-%m-%d")
			date = date + " 00:00:00"
		try:
			phrase = post_infoes[1].get_text(" ", strip = True)
		except:
			phrase = "0"
		phrase = post_wash(phrase)
		url = post.find("a")["href"]
		#뉴스 url 에 들어가서 img를 가져오기위한 작업
		domain = Domain_check(url)	#뉴스 url 도메인
		driver_page = URLparser(url)
		bs_page = BeautifulSoup(driver_page, 'html.parser')
		try:
			img = bs_page.find("head").find("meta", {"property": "og:image"})['content']
		except:
			try:
				if bs_page.find("body").find("img") is None:
					img = 1
				else:
					img = bs_page.find("body").find("img")['src']
					if 1000 <= len(img):
						img = 1
					else:
						if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
							pass
						elif img.startswith("//"):
							img = "http:" + img
						else:
							img = domain + img
			except:
				 img = 1
		if img != 1:
			if img_size(img):
				pass
			else:
				img = 1

		post_data['title'] = title.upper()
		post_data['author'] = author.upper()
		post_data['date'] = date
		post_data['post'] = phrase.lower()
		post_data['img'] = img
		post_data['url'] = url

		print(date, "::::", title)

		#게시물의 날짜가 end_date 보다 옛날 글이면 continue, 최신 글이면 append
		if str(date) <= end_date:
			continue
		else:
			post_data_prepare.append(post_data)
			
	return post_data_prepare



#url을 받으면 Page를 변환시켜서, 변환된 url 반환
def Change_page(url, page):
	url_done = url + str(page)

	return url_done


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain