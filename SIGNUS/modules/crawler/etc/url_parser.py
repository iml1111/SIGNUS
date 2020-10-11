import requests
import time

header = {
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
			AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
			"Accept":"text/html,application/xhtml+xml,application/xml;\
			q=0.9,imgwebp,*/*;q=0.8"
		}


def URLparser(URL):	#header을 지정하고 requests.get 하는 함수
	try:
		html = requests.get(URL, verify = False, headers = header).text
	except:
		time.sleep(3)
		print("Connection Error")
		try:
			html = requests.get(URL, verify = False,  headers = header).text
		except:
			print("Connection Failed")
			return None
	return html

def URLparser_decode(URL, enc):	#어떤 사이트는 decoding를 안 할 떄가 있다. 그럴 때, 내가 직접 decoding을 해주는 것이다.
	try:
		html = requests.get(URL, verify = False,  headers = header).content.decode(enc)
	except:
		time.sleep(3)
		print("Connection Error")
		try:
			html = requests.get(URL, verify = False,  headers = header).content.decode(enc)
		except:
			print("Connection Failed")
			return None
	return html	

def URLparser_EUCKR(URL):
	try:
		html = requests.get(URL, verify = False,  headers = header)
		html.raise_for_status()
		html.encoding='EUC-KR'
		html = html.text
	except:
		time.sleep(3)
		print("Connection Error")
		try:
			html = requests.get(URL, verify = False,  headers = header)
			html.raise_for_status()
			html.encoding='EUC-KR'
			html = html.text
		except:
			print("Connection Failed")
			return None
	return html

def URLparser_UTF8(URL):
	try:
		html = requests.get(URL, verify = False,  headers = header)
		html.raise_for_status()
		html.encoding='UTF-8'
		html = html.text
	except:
		time.sleep(3)
		print("Connection Error")
		try:
			html = requests.get(URL, verify = False,  headers = header)
			html.raise_for_status()
			html.encoding='UTF-8'
			html = html.text
		except:
			print("Connection Failed")
			return None
	return html