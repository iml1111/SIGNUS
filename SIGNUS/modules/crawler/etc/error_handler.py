from modules.crawler.dbs.mongo.db_health import url_health_check
from datetime import datetime
import time
from platform import platform
import os

def error_logging(e, URL, page_url, db):
	log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	log_info = URL['info']
	log_url = page_url
	print("[ERROR]=====================================================================")
	print(log_time, " :: ", log_info, "\nURL :: ", log_url)
	print(type(e), "\n", e, "\n\n\n\n")
	f = open(os.getenv("SIGNUS_CRAWLER_ERROR_LOG_PATH"),'a')

	f_data = "[ERROR]=====================================================================\n"
	f_data = f_data + log_time + " :: " + log_info + "\nURL :: " + log_url + "\n"
	f_data = f_data + str(type(e)) + "\n" + str(e) + "\n\n"
	f.write(f_data)
	f.close()
	time.sleep(2)

def error_handler(e, URL, page_url, db):
	# 앞으로 5번동안 이 사이트 크롤링 일시중지
	url_health_check(URL['url'], db)
	error_logging(e, URL, page_url, db)

def continue_handler(target, URL, page_url):
	log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	log_info = URL['info']
	log_url = page_url
	f = open(os.getenv("SIGNUS_CRAWLER_LOG_PATH"),'a')

	f_data = "[Continue]==================================================================\n"
	f_data = f_data + log_time + " :: " + log_info + "\nURL :: " + log_url + "\n"
	f_data = f_data + "Now Crawling :: " + target + "\n\n\n\n"
	f.write(f_data)
	f.close()