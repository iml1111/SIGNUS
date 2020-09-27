import re
def post_wash(text):
	data = re.sub(r'\s+'," ", text)
	return data