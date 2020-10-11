from selenium import webdriver
from platform import platform
import os
# def chromedriver():
# 	options = webdriver.ChromeOptions()
# 	options.add_argument('headless')
# 	options.add_argument('window-size=1920x1080')
# 	options.add_argument("disable-gpu")
# 	options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome")
# 	options.add_argument("lang=ko_KR")

# 	path = os.getenv("SIGNUS_CHROMEDRIVER_PATH")

# 	if platform().startswith("Windows"):
#     		driver = webdriver.Chrome('../chromedriver.exe', options=options)
# 	else:
#     		driver = webdriver.Chrome(path, options=options)

# 	return driver

def chromedriver():
	path = os.getenv("SIGNUS_CHROMEDRIVER_PATH")
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument("--ignore-ssl-errors=true")
	chrome_options.add_argument("--ssl-protocol=any")
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome")

	driver = webdriver.Chrome(executable_path=path,options=chrome_options)
	return driver


