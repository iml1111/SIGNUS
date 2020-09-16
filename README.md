# SIGNUS
대학생을 위한 뉴스피드

# Tokenizer
입력된 문자열의 명사 추출 및 리스트의 형태로 반환한다.
```
from modules.tokenizer import Tokenizer

msg = "사람은 밥을 먹는다"

obj = Tokenizer()
result = obj.get_tk(msg)
print(result)

>>> ['사람', '밥']
```