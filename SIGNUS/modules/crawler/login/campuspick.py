from modules.crawler.login import all_login
import time



login_data = all_login.campuspick()
ID = login_data[0]
PW = login_data[1]

#로그인 하는 cord
def login(driver):
	
	driver.get('https://www.campuspick.com/login')
	driver.implicitly_wait(3)
	
	####로그인정보 보냄####
	driver.find_element_by_name('userid').send_keys(ID)
	driver.find_element_by_name('password').send_keys(PW)
	####로그인버튼 누르기####
	driver.find_element_by_xpath('//*[@id="container"]/div[2]/div/input[3]').click()
	time.sleep(3)

	return driver