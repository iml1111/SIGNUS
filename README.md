# SIGNUS
대학생을 위한 뉴스피드

# Tokenizer
입력된 문자열의 명사 추출 및 리스트의 형태로 반환한다.
``` python
from modules.tokenizer import Tokenizer

msg = "사람은 밥을 먹는다"

obj = Tokenizer()
result = obj.get_tk(msg)
print(result)

>>> ['사람', '밥']
```

# Recommender
FastText 기반의 문서 임베딩 벡터 연산기

## Trainer
``` python
from modules.recommender.fasttext.trainer import Trainer

# 학습용 데이터
sent_1 = [
    ['computer', 'aided', 'design'],
    ['computer', 'science'],
    ['computational', 'complexity'],
    ['military', 'supercomputer'],
    ['central', 'processing', 'unit'],
    ['onboard', 'car', 'computer'],
]

# 전이 학습용 데이터
sent_2 = [
    ['computer', 'design', 'aided'],
    ['computer', 'scienc'],
    ['I', 'love', 'him'],
    ['military', 'supercomputer'],
    ['I', 'love', 'you'],
]

# 트레이너 로드 및 하이퍼파라미터 세팅
trainer = Trainer() 
trainer.set_params(
    vec_size=10,
    windows=3,
    min_count=1,
    iteration=1,
    workers=1
)

# 학습용 코포라 세팅 및 학습
trainer.set_corpora(sent_1) 
trainer.train()

# 전이학습용 코포라 세팅 및 학습
trainer.set_corpora(sent_2)
trainer.update()

# 모델 저장 및 불러오기 메소드
trainer.save_model(path="./test_model")
trainer.load_model(path="./test_model")

```

## Recommender
Recommender 클래스를 사용하기 위해서는 사전에 학습된 모델이 필요하다.
해당 모델의 경로를 클래스 선언시의 인자로 넘겨 모델을 임포트할 수 있다.
``` python
from modules.recommender.fasttext import Recommender
# Path to FastText model
recommender = Recommender("./ft/soojle_ft_model")


# 입력된 토큰, 토큰 리스트에 대하여 가장 의미상 가까운 단어 num 개를 반환
>>> recommender.doc2words("python")
[('sql', 0.900479257106781), ('tensorflow', 0.8909381628036499), ('javascript', 0.8879169821739197), ('ript', 0.8836684823036194), ('opengl', 0.8771063089370728), ('프로그래밍', 0.8725562691688538), ('nosql', 0.8630207777023315), ('자바스크립트', 0.861074686050415), ('framework', 0.859409749507904), ('nodejs', 0.8563205003738403)]


# 입력된 토큰, 토큰 리스트에 대한 임베딩 벡터 반환
>>> vec1 = recommender.doc2vec("python")
>>> vec1
array([ 0.02856478, -0.11470377,  0.01810528,  0.06545372, ...], dtype=float32)


# 입력된 벡터에 대하여 가장 의미상 가까운 단어 num 개를 반환
>>> recommender.vec2words(vec)
[('python', 1.0), ('sql', 0.900479257106781), ('tensorflow', 0.8909381628036499), ('javascript', 0.8879169821739197), ('ript', 0.8836684823036194), ('opengl', 0.8771063089370728), ('프로그래밍', 0.8725562691688538), ('nosql', 0.8630207777023315), ('자바스크립트', 0.861074686050415), ('framework', 0.859409749507904)]

# 두 토큰 or 토큰 리스트에 대한 의미적 유사도 반환
>>> recommender.doc_sim("java", "python")
0.8159679
>>> recommender.doc_sim("java","짜장면")
-0.37807456

# 두 임베딩 벡터간의 의미적 유사도 반환
>>> vec2 = recommender.doc2vec("java")
>>> recommender.vec_sim(vec1, vec2)
0.8159679

# 해당 토큰을 모델이 알고 있는지 검사
>>> recommender.is_in_dict("python")
True
>>> recommender.is_in_dict("서정민")
False
```