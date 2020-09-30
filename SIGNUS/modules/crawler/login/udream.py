import requests
from modules.crawler.login import all_login



login_data = all_login.udream()
ID = login_data[0]
PW = login_data[1]

#로그인 하는 cord
def login():
	data = {"rUserid":ID, "rPW":PW, "pro":"1"}
	s = requests.Session()
	# url 에 로그인 데이터를 넘겨줌
	page = s.post("https://udream.sejong.ac.kr/main/loginPro.aspx", data = data)
	#로그인 쿠키값을 만들어줌.
	s.cookies.set("mauth","1")
	s.cookies.set("hn_mauth","1")
	s.cookies.set("hn_ck_login",page.text[169:249])

	return s