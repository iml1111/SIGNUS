from bs4 import BeautifulSoup
from modules.crawler.etc.url_parser import URLparser
from modules.crawler.etc.url_parser import URLparser_EUCKR
from modules.crawler.etc.url_parser import URLparser_UTF8

from modules.crawler.dbs.mongo.db_manager import db_manager
from modules.crawler.dbs.mongo.db_manager import get_lastly_post
from modules.crawler.dbs.mongo.db_manager import push_lastly_post
from modules.crawler.dbs.mongo.db_health import is_crawling

from modules.crawler.list.date_cut import date_cut
from modules.crawler.etc.error_handler import error_handler
from modules.crawler.etc.error_handler import continue_handler

import time

from modules.crawler.sj_crawling import sj1, sj2, sj3, sj4, sj5, sj6, sj7, sj8, sj9,\
sj10, sj11, sj12, sj13, sj14, sj15, sj16, sj17, sj18,\
sj19, sj20, sj21, sj23, sj24, sig25, sig26, sig27, sig28,\
sj29, sj30, sj31, sj32, sj33, sj34, sig35, sig36, sig37,\
sj38, sig39, sj40, sj41, sj42, sig43, sj44,\
sig45, sig46, sig47, sig48, sig50, sig51, sig52, sig53, sig54,\
sig55, sig56, sig57

def Crawling(URL, db):
	driver = None
	info_name = URL['info'].split('_')
	crawling_name = info_name[0]	#게시판 크롤링 선택
	page = 1
	main_url = URL['url']	#게시판 url 추출 : 페이지 바꾸는 데에 사용
	page_url = eval(crawling_name + '.Change_page(main_url, page)')	#현재 페이지 포스트 url 반환
	end_date = date_cut(URL['info'])	# end_date 추출
	if crawling_name in ["sj4","sj17","sj19","sj20","sj23","sj30","sj34","sj44","sig56"]:		# 제외 게시판
		return
	

	#현재 크롤링하는 게시판 info 출력
	print("Target : ", URL['info'])
	continue_handler(URL['info'], URL, page_url)
	#크롤링 유무판단
	if is_crawling(db, URL['info']) == False:
		return

	while True:
		if crawling_name in ["sj10", "sj11","sj13"]: #추후에 보수 후에 사전으로 각 함수 실행하기
			eval(crawling_name + '.init(URL, end_date, db)')
			break
		if crawling_name in ["sig26", "sig27", "sig28", "sj44", "sig50", "sig51","sig55","sig56","sig57"]:
			lastly_post = get_lastly_post(URL, db)
			print("lastly_post : ",lastly_post)
		try:
			print("\npage_url :::: ", page_url)	#현재 url 출력
			print("Page : ", page)				#현재 페이지 출력
			#driver_page 생성---------------------------
			# if crawling_name in ['sj10']:
			# 	driver_page = URLparser_EUCKR(page_url)
			if crawling_name in ['sj12']:
				driver_page = URLparser_UTF8(page_url)
			else:
				driver_page = URLparser(page_url)
			#-------------------------------------------
			#Selenium을 쓰는 경우----------------------------------------------------------------------------------------------
			if crawling_name in ["sig26", "sig27", "sig28", "sj29", "sj38", "sj44", "sig50", "sig51", "sig52","sig55","sig56","sig57"]:
				data = eval(crawling_name + '.Parsing_list_url(URL, page_url, driver)')
				driver = data[0]
				post_urls = data[1]
			# elif crawling_name in ["sj30"]:#---------------------------세종대역 예외처리
			# 	data = eval(crawling_name + '.Parsing_list_url(URL, page_url, lastly_post, db, driver)')
			# 	driver = data[0]
			# 	post_urls = data[1]
			#Requests를 쓰는 경우----------------------------------------------------------------------------------------------
			else:
				#로그인을 하는 경우-------------------------------------------------------------------------------
				if URL['login'] == 1:
					post_urls = eval(crawling_name + '.Parsing_list_url(URL, page_url)')
				#로그인을 하지않는 경우---------------------------------------------------------------------------
				else:
					if driver_page is None:		#Connect Failed 이면 break
						error_handler("driver_none", URL, page_url, db)
						break
					else:
						#parsing 형태--------------------------------------------------
						# if crawling_name in ['sj10']:
						# 	bs_page = BeautifulSoup(driver_page, 'lxml')
						# else:
							bs_page = BeautifulSoup(driver_page, 'html.parser')
						#--------------------------------------------------------------
                    #20대연구소 예외
					if crawling_name == "sig47":
						pageidx = page_url.split('=')[1]
						post_urls = eval(crawling_name + '.Parsing_list_url(URL, bs_page, pageidx)')
					#네이버 뉴스기사
					elif crawling_name == "sig54":
						post_urls = eval(crawling_name + '.Parsing_list_url(URL, page_url)')
					else:		
						post_urls = eval(crawling_name + '.Parsing_list_url(URL, bs_page)')                    
				#-----------------------------------------------------------------------------------------------
			#-----------------------------------------------------------------------------------------------------------------
			#get_post_data 형식 : [게시글정보dictionary, title, date]-------------------------------------------------------------------------------------------------------
			#date 규격은 "0000-00-00 00:00:00"
			post_data_prepare = []
			for post_url in post_urls:
				
				#Selenium인 경우--------------------------------------------------------------------------------------------------------------------
                #------------------게시판 규격인 경우
				if crawling_name in ['sj29', 'sig52']:
					try:
						get_post_data = eval(crawling_name + '.Parsing_post_data(driver, post_url, URL)')
					except:
						try:
							get_post_data = eval(crawling_name + '.Parsing_post_data(driver, post_url, URL)')
						except:
							continue
				#----------------게시판 규격이 아닌 경우
				elif crawling_name in ['sig26', 'sig27', 'sig28', 'sj44', 'sig50', 'sig51',"sig55","sig56","sig57"]:
					try:
						data = eval(crawling_name + '.Parsing_post_data(driver, post_url, URL, lastly_post)')
					except:
						try:
							data = eval(crawling_name + '.Parsing_post_data(driver, post_url, URL, lastly_post)')
						except Exception as e:
							print(e)
						except:
							continue
					# data = eval(crawling_name + '.Parsing_post_data(driver, post_url, URL, lastly_post)')

					post_data_prepare = data[0]
					lastly_post = data[1]
					if lastly_post is None:
						pass
					else:
						push_lastly_post(URL, lastly_post, db)
				#Requests인 경우--------------------------------------------------------------------------------------------------------------------
				else:
					#driver_post 생성--------------------------------
					if crawling_name in ["sj21","sj5", "sj8", "sj16"]: #---driver_post가 필요없는 경우
						pass
					elif crawling_name in ['sj33']:
						driver_post = URLparser_EUCKR(post_url)
					elif crawling_name in ['sj12']:
						driver_post = URLparser_UTF8(post_url)
					else:
						driver_post = URLparser(post_url)
					#------------------------------------------------
					#-----------------------------------------------------------------------------------------------위키백과 구조
					if crawling_name in ['sj21']:
						try:
							get_post_data = eval(crawling_name + '.Parsing_post_data(post_url, URL)')
						except:
							try:
								get_post_data = eval(crawling_name + '.Parsing_post_data(post_url, URL)')
							except:
								continue
					#-----------------------------------------------------------------------------------------------게시판 규격이 아닌 구조
					elif crawling_name in ["sj5", "sj8", "sj16"]:
						try:
							post_data_prepare = eval(crawling_name + '.Parsing_post_data(post_url, URL)')
						except:
							try:
								post_data_prepare = eval(crawling_name + '.Parsing_post_data(post_url, URL)')
							except:
								continue
						break
					#-----------------------------------------------------------------------------------------------게시판 규격인 구조
					else:
						if driver_post is None:		#Connect Failed 이면 continue
							error_handler("driver_none", URL, page_url, db)
							break
						else:
							#parsing 형태-------------------------------------------
							# if crawling_name in ['sj10']:
							# 	bs_post = BeautifulSoup(driver_post, 'lxml')
							# elif crawling_name in ['sj12']:
							if crawling_name in ['sj12']:
								bs_post = driver_post
							else:
								bs_post = BeautifulSoup(driver_post, 'html.parser')
							#-------------------------------------------------------
						try:
							get_post_data = eval(crawling_name + '.Parsing_post_data(bs_post, post_url, URL)')
						except:
							try:
								get_post_data = eval(crawling_name + '.Parsing_post_data(bs_post, post_url, URL)')
							except:
								continue
				#-----------------------------------------------------------------------------------------------------------------------------------
				
				#post_data_prepare이 이미 완성된 경우-----------------------------------------------------------------------
				if crawling_name in ["sj5", "sj8", "sj16", "sig26", "sig27", "sig28", "sj44", "sig50", "sig51","sig55","sig56","sig57"]:
					pass
				#post_data_prepare이 완성되지 않은 경우---------------------------------------------------------------------
				# 네이버 뉴스 기사
				elif crawling_name == "sig54":
					if get_post_data == None:	#잘못된 포스트 데이터인 경우
						continue
					for item in get_post_data:	
						date = item["date"]
						#게시물의 날짜가 end_date 보다 옛날 글이면 continue, 최신 글이면 append
						if str(date) <= end_date:
							continue
						else:
							post_data_prepare.append(item)
				else:
					if get_post_data == None:	#잘못된 포스트 데이터인 경우
						continue
					title = get_post_data[1]
					date = get_post_data[2]
		
					print(date, "::::", title)	#현재 크롤링한 포스트의 date, title 출력
		
					#게시물의 날짜가 end_date 보다 옛날 글이면 continue, 최신 글이면 append
					if str(date) <= end_date:
						continue
					else:
						post_data_prepare.append(get_post_data[0])
			#----------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------------------------------------------------------
			add_cnt = db_manager(URL, post_data_prepare, db)
			print("add_OK : ", add_cnt)	#DB에 저장된 게시글 수 출력
		
			#dirver 종료 [Selenium 을 사용했을 시]
			if crawling_name in ["sig26", "sig27", "sig28", "sj29", "sj38", "sj44", "sig50", "sig51", "sig52","sig55","sig56","sig57"]:
				driver.quit()
			
			#DB에 추가된 게시글이 0 이면 break, 아니면 다음페이지
			if add_cnt == 0:
					break
			else:
				page += 1
				page_url = eval(crawling_name + '.Change_page(main_url, page)')
		# Error handler : 만약 크롤링이 실패했을 경우, 에러를 logging 하고 크롤링을 중단한다.
		except Exception as e:
			error_handler(e, URL, page_url, db)
			break
