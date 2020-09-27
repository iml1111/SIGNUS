from modules.crawler.login import all_login
import time



login_data = all_login.everytime()
ID = login_data[0]
PW = login_data[1]

#로그인 하는 cord
def login(driver):
	
	driver.get('https://everytime.kr/login')
	driver.implicitly_wait(3)
	
	####로그인정보 보냄####
	driver.find_element_by_name('userid').send_keys(ID)
	driver.find_element_by_name('password').send_keys(PW)
	####로그인버튼 누르기####
	driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()
	time.sleep(3)

	return driver