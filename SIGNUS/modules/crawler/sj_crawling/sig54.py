from datetime import timedelta
import datetime

from modules.crawler.etc.url_parser import URLparser
from bs4 import BeautifulSoup

from modules.crawler.list.url_list import List
from modules.crawler.list.date_cut import date_cut_dict
from modules.crawler.etc.post_wash import post_wash
from modules.crawler.etc.img_size import img_size
#게시판 page_url 을 받으면, 그 페이지의 포스트 url 들을 반환
#
#네이버 뉴스의 경우, 
#한 페이지에 10개의 기사들의 li 태그들을 가져와야 하기에
#각 기사들의 url이 필요가 없다 
def Parsing_list_url(URL, page_url):
	List = []
	List.append(page_url)
	return List

# 날짜 form 변경
def change_date_form(dateform):
	#일 => 7일 max
	#시간 => 23시간
	#분 =>59분
	#초 => 59초
	current_time = datetime.datetime.now()
	date=''
	timeCheck = ['일','시간','분','초']
	for time in timeCheck:
		if time in dateform:
			if time == "일":
				parsing_date = int(dateform.split("일")[0])
				date = str(current_time - datetime.timedelta(days = parsing_date)).split('.')[0]
				return date
			elif time == "시간":
				parsing_date = int(dateform.split("시간")[0])
				date = str(current_time - datetime.timedelta(hours = parsing_date)).split('.')[0]
				return date
			elif time == "분":
				parsing_date = int(dateform.split("분")[0])
				date = str(current_time - datetime.timedelta(minutes= parsing_date)).split('.')[0]
				return date
			elif time == "초":
				parsing_date = int(dateform.split("초")[0])
				date = str(current_time - datetime.timedelta(seconds = parsing_date)).split('.')[0]
				return date		
	date = str(dateform).split('.')[0]
	return date

#포스트 url을 받으면, 그 포스트의 정보를 dictionary 형태로 반환
def Parsing_post_data(bs, post_url, URL):
	List = []
	posts = bs.find("ul",{"class":"type01"}).find_all("li")
	for post in posts:
		if post.has_attr('id') == True:
			List.append(post)
	
	return_data = []
	for item in List:
		post_data = {}
		title = item.find("dt").get_text(" ", strip = True)
		author = ''
		date = ''
		domain = ''
		date_parsed = item.find("dd",{"class":"txt_inline"}).get_text(" ",strip = True).split(" ")
		list_size = len(date_parsed)
		if list_size <= 4: # ['출처','n시간','전','보내기'] , ['출처','2000-00-00','보내기']
			date = change_date_form(date_parsed[1])
		elif list_size == 5: #['출처','n시간','전','네이버뉴스','보내기'],['출처','위치','n시간','전','보내기']
			if '네이버뉴스' in date_parsed:
				date = change_date_form(date_parsed[1])
			else :
				date = change_date_form(date_parsed[2])
		elif list_size == 6: #['출처','위치','시간','전','네이버뉴스','보내기']
			date = change_date_form(date_parsed[2])
		else: #['출처','언론사','선정','n시간','전','보내기']
			date = change_date_form(date_parsed[3])
		post = item.find("dd", {"class": "txt_inline"}).find_next('dd').get_text(" ", strip = True)
		post = post_wash(post)		#post 의 공백을 전부 제거하기 위함
		list_url = item.find("dt").find("a")['href']
		driver_post = URLparser(list_url)
		bs_post = BeautifulSoup(driver_post, 'html.parser')
		if bs_post.find("meta", {"property": "og:image"}) is None:
			img = 7
		else:
			try:
				img = bs_post.find("meta", {"property": "og:image"}).get("content")	#게시글의 첫번째 이미지를 가져옴.
				if 1000 <= len(img):
					img = 7
				else:
					if img.startswith("http://") or img.startswith("https://"):		# img가 내부링크인지 외부 링크인지 판단.
						pass 
					elif img.startswith("//"):
						img = "http:" + img
					else:
						img = domain + img
			except:
				img = 7
		if img != 7: 
			if img_size(img):
				pass
			else:
				img = 7
		
		post_data['title'] = title.upper()
		post_data['author'] = author
		post_data['date'] = date
		post_data['post'] = post.lower()
		post_data['img'] = img
		post_data['url'] = list_url

		return_data.append(post_data)
	return return_data



#url을 받으면 Page를 변환시켜서, 변환된 url 반환
def Change_page(url, page):	
	parsed_url = url.split("&start=")
	url_done = parsed_url[0] + "&start=" + str(page) + parsed_url[1]
	return url_done


#입력된 url의 도메인 url 반환
def Domain_check(url):
	domain = url.split('/')[0] + '//' + url.split('/')[2]	#도메인 url 추출
	# domain = https://www.example.com
	return domain