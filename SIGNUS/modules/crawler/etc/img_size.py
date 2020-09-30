import requests
from PIL import Image
from io import BytesIO



#img 파일의 크기를 체크하여 만약 가로 세로 길이가 (50by50)px 이하이라면 False 반환, 아니면 True 반환
def img_size(url):
	try:
		html = requests.get(url).content
	except:
		return False
	try:
		img = Image.open(BytesIO(html))
	except:
		return False

	try:
		width, height = img.size
	except:
		return False

	if width <= 50 and height <= 50:
		return False
	else:
		return True