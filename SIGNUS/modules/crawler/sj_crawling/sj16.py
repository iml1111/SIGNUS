import datetime
from modules.crawler.login import udream

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
	domain = Domain_check(URL['url'])	#뉴스 url 도메인
	post_data_prepare = []
	end_date = date_cut(URL['info'])
	now = datetime.datetime.now().strftime("%Y-%m-%d")

	try:
		posts = bs.findAll("div", {"class": "article-board"})[1].find("tbody").findAll("tr")
	except:
		try:
			posts = bs.findAll("div", {"class": "article-board"})[1].findAll("tr")
		except:
			posts = []

	for post in posts:
		post_data = {}
		if post.find("td", {"class": "td_article"}) is not None:
			title = post.find("td", {"class": "td_article"}).find("a", {"class": "article"}).get_text(" ", strip = True)
			if post.find("td", {"class": "td_article"}).find("a", {"class": "article"}).find("span") != -1:
				title_plus = post.find("td", {"class": "td_article"}).find("a", {"class": "article"}).find("span")
				if title_plus is None:
					pass
				else:
					title = post_wash(title)
					title = title.replace(" ", "")
			else:
				pass
			author = post.find("td", {"class": "td_name"}).find("a").text.strip()
			if author.find("관리자") != -1:
				author = "0"
			date = post.find("td", {"class": "td_date"}).text.strip()
			if date[2] == ':':
				date = str(now) + " " + date + ":00"
				date = str(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
			else:
				date = date + " 00:00:00"
				date = str(datetime.datetime.strptime(date, "%Y.%m.%d. %H:%M:%S"))
			phrase = "0"
			url = post.find("td", {"class": "td_article"}).find("a", {"class": "article"})["href"]
			url = domain + url
			img = 2
	
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
		else:
			if post.find("span", {"class": "aaa"}) is not None:
				print(post.find("span", {"class": "aaa"}))
				title = post.find("span", {"class": "aaa"}).find("a").text.strip()
				author = post.find("td", {"class": "p-nick"}).text.strip()
				date = post.find("td", {"class": "view-count m-tcol-c"}).text.strip()
				if (date.find(":") != -1):
					date = datetime.datetime.now().strftime("%Y.%m.%d.")
				date = date + " 00:00:00"
				date = str(datetime.datetime.strptime(date, "%Y.%m.%d. %H:%M:%S"))
				phrase = "0"
				url = post.find("span", {"class": "aaa"}).find("a")['href']
				url = domain + url
				img = 2

				post_data['title'] = title.upper()
				post_data['author'] = author.upper()
				post_data['date'] = date
				post_data['post'] = phrase.upper()
				post_data['img'] = img	
				post_data['url'] = url
		
				print(date, "::::", title)
				#게시물의 날짜가 end_date 보다 옛날 글이면 continue, 최신 글이면 append
				if str(date) <= end_date:
					continue
				else:
					post_data_prepare.append(post_data)
			else:
				pass

			
	return post_data_prepare



#url을 받으면 Page를 변환시켜서, 변환된 url 반환
def Change_page(url, page):
	url_done = url + str(page)

	return url_done


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출

	return domain