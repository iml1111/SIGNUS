import requests
from modules.crawler.login import all_login
import time



login_data = all_login.daum()
ID = login_data[0]
PW = login_data[1]

#로그인 하는 cord
def login(driver):
	
	#driver.get('https://logins.daum.net/accounts/loginform.do')	#이전버젼 
	driver.get('https://logins.daum.net/accounts/signinform.do')	#수정버젼
	driver.implicitly_wait(3)
	
	####로그인정보 보냄####
	driver.find_element_by_name('id').send_keys(ID)
	driver.find_element_by_name('pw').send_keys(PW)
	####로그인버튼 누르기####
	driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
	time.sleep(3)

	return driver