# SIGNUS - 대학생을 위한 뉴스피드
![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MJzCCiiBrsRdu9_cGtV%2F-MJzFcvBv0K6iac8qhXC%2Fimage.png?alt=media&token=ca209931-afb6-4daa-9657-4048975508bb)

![image](https://user-images.githubusercontent.com/29897277/117573942-b1c77300-b115-11eb-9d9e-66cfeafb5f08.png)



## 프로젝트 요약

대학교는 재학생의 편리한 학교생활을 위해 여러 커뮤니티 및 공지 등을 통해 유용한 정보를 게시하거나 공지한다. 그 안에는 학교의 메인 홈페이지 외에도 학과 및 동아리에서 각각 개설되는 웹 사이트, 학생들이 자발 적으로 만든 커뮤니티, 플랫폼까지 포함하면 한 학교에서만 관련 사이트가 수백 개에 다다르게 되었다.

그러나 이러한 환경에 반해 실제 대학교 관련 정보를 탐색하는 상당히 불편하다는 평을 받고 있다. 서비스 자체의 접근성, 알려지지 않아 가치 면에 비해 사용량이 저조한 서비스, 여러 곳에 흩어져 있고 중복으로 존재하는 정보 등을 통해 구글을 비롯한 통합 검색 엔진으로도 찾을 수 없는 정보가 점점 증가하고 있다. 

본 프로젝트는 이러한 문제점을 해결하기 위해 해당 학교 관련된 웹상의 모든  정보를 수집하여 통합한 접근성이 높은 서비스를 제공함으로 학생들의 정보 접근성을 높여 더 편리한 학교생활에 임할 수 있도록 하는 서비스 제공을 목표로 한다. 

흩어져 있던 정보들을 한 곳으로 통합시켜 필요한 정보의 탐색을 용이하게 하고, 사용자의 액션을 수집하여 대학교 전체의 흐름을 파악하는 유의미한 가치의 정보를 수집할 수 있다. 본 프로젝트를 수행함으로써,  학교 내의 모든 정보를 체계화하고 접근성을 높여 정보의 소비량을 증진시키고 학생들이 보다 편리하게 학교생활에 임하는 것이 가능할 것이라 기대한다.



## 솔루션

시그너스는 아래와 같은 솔루션을 통해 문제를 해결하고자 한다.



### 정보의 통합

![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MK8UQpTJMOrm-kfGTjy%2F-MK9pBqX5XgpTdrNYy6q%2Fimage.png?alt=media&token=fb4a9595-1916-44e2-bf36-693375200bd9)

- 시그너스는 아래와 같은 솔루션을 통해 문제를 해결하고자 한다.
- 지속적으로 좋은 정보를 제공하는 서비스 발굴 및 연동하여, 사용자들이 하나의 서비스로 여러 정보를 접할 수 있도록 한다.



### 관심사 추천

![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MK8UQpTJMOrm-kfGTjy%2F-MK9pG7mq_Y9Iwsxw1N7%2Fimage.png?alt=media&token=8a4a9794-d477-4345-bff8-2f671d0eddb7)

- 실시간으로 수집된 정보를 수집 및 체계화한다.

- 딥러닝 기반 기술로 수집된 정보들의 주제 및 관심사 분석하여 군집화한다.  이를 통해 복수의 게시물에 대한 카테고리 자동화가 이루어진다.

- 시그너스는 유저가 서비스 내에서 활동한 모든 히스토리를 분석하여  사용자들이 원하는 정보를 관심사에 맞게 추천한다.




### 지역 기반 광고 플랫폼

- 대학교를 중심으로 한 지역 기반 공동체 커뮤니티를 형성한다.

- 지역성을 이용한 접근성 높은 광고 플랫폼을 구축하여, 지역 간 사용자들의 소통을 확대시킬 수 있다.

- 지역 기반으로 광고 단가를 최소화함으로써 개인 사업자, 지역 소상공인 등도 손쉽게 이용할 수 있는 광고/홍보 플랫폼 구축한다.



## 시그너스 추천 시스템

![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MKh5F3Z28IA0VzUym5W%2F-MKhE8wViydTzRnYmjhC%2F%EC%A0%9C%EB%AA%A9%20%EC%97%86%EC%9D%8C.png?alt=media&token=72a3c79f-cdd5-4922-96b3-a0fd954af4f4)

## 추천 뉴스피드

추천 뉴스피드는 사용자의 모든 액션을 기반으로 관심 분야를 예측하고 그와 관련된 게시물 목록을 사용자에게 제시한다. 추천 뉴스피드에서 게시물을 선별하는 알고리즘은 다음과 같다. (이하 X는 불확정 변수로 정의한다)

1. DB 내에 저장된 모든 게시물 데이터를 **최신 시간  순으로 정렬**한다.
2. **상위 X개 데이터를  제외하고 추천 목록에서 제거**한다.
3. 각 문서의 사용자-문서 유사도**(Recommendation Score)** 값을 구해 높은 순으로 정렬한다.
4. 해당 문서들을 추천 뉴스피드에 반환한다. 

‌

## 사용자-문서 유사도(Recommendation Score)

사용자-문서 유사도란, 시그너스에서 제시되는 여러 정보, 콘텐츠들에 대하여 각각의 사용자에 관심사나 얼마나 일치하는 지를 수치화시킨 값을 말한다. 뉴스피드 추천시, 시그너스는 각 사용자의 관심사 정보를 수집 및 분석하여 모든 콘텐츠에 대하여 사용자가 해당 콘텐츠에 관심이 있을 확률을 수치로써 도출한다. 그리고 해당 수치를 통해 콘텐츠들의 Ranking을 메겨 결과값을 반환하는 것으로 추천이 이루어지게 된다.

이러한 사용자와 콘텐츠간의 추천 점수를 평가하는 항목은 다음과 같다.

- **이 콘텐츠는 사용자가 평소에 관심이 있던 분야 or 주제인가?**
- **해당 콘텐츠는 사용자에게 질 좋은(신뢰도 있는) 정보를 제공하는가?**

‌

## 사용자 문서 유사도 수식 

각 사용자에게 적절한 뉴스피드를 생성하는 과정에 앞서, 사용자와 문서 간의 관련성을 수식화하는 과정은 다음과 같다.

![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MKPdz8Oe7-IrgHlTnQX%2F-MKPfmiJbhtQ57J0B_8e%2Fimage.png?alt=media&token=004ce94d-ba98-445c-a459-086c933debae)



### Topic Similarity(ToS)

사용자와 문서 간의 주제 유사도를 나타내는 변수이다. 콘텐츠들은 주제 분석으로 통해 고유의 Latent  Embedding Vector를 가지게 된다. 이러한 콘텐츠들 사이에 두 벡터간의 유사도를 판단하기 위해 **Cosine Similarity**를 사용한다. 사용자와 문서의 ToL(Topic List)이 다음과 같이 주어졌을 때, 다음과 같이 유사도를 구할 수 있다.

![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MKPdz8Oe7-IrgHlTnQX%2F-MKPiT11a1cIS0fyO2HU%2Fimage.png?alt=media&token=6a299eb1-72db-40d7-8694-5e1579be898a)

### Tag Similarity(TaS)

사용자와 문서 간의 보유한 태그 유사도를 나타내는 변수이다. 태그의 경우, 각 태그에 대한 가중치 정보를 갖고 있지 않기 때문에 다음과 같이 TaL(태그 리스트)의 교집합 값을 통해 결과를 도출한다.

![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MKPdz8Oe7-IrgHlTnQX%2F-MKPi_-xrL8b7GEuZKnk%2Fimage.png?alt=media&token=97aa5853-4aa0-441d-82ab-d7eaaac884ea)



### Issue Score(IS)

해당 게시물의 인기도를 나타내는 변수이다. 인기도의 지표로 사용되는 수치는 해당 단일 글의 **"좋아요" 횟수**와 **조회수**이다.

**MaxInterests** : 현재까지 모든 게시물 중, 최대 "좋아요" 수 

 **MaxViews** : 현재까지 모든 게시물 중, 최대 조회수  

**Interests**: 현재 게시물의 좋아요 수 

 **Views:** 현재 게시물의 조회수  

**X:** 불확정 변수

![img](https://gblobscdn.gitbook.com/assets%2F-MHBtcixyD3pB5WEsMLf%2F-MKPdz8Oe7-IrgHlTnQX%2F-MKPioQRoyD-Ox8L7Rqq%2Fimage.png?alt=media&token=77be7144-84b9-426e-a005-fe12615592d9)

Enter a caption for this image (optional)



### rand(X)

뉴스피드에 지속적으로 새로운 글을 표출하기 위한 어떠한 변수에도 종속되지 않는 랜덤 변수이다. 약간의 랜덤 값을 추가하여, 강제로 추천 성능을 떨어트리는 대신에 무작위성을 부가함으로써 추천 리스트가 다채로워지게 할 수 있다.

### except(X)

관리자 혹은 시스템이 직접 뉴스피드 생성에 관여하고 접근할 수 있도록 하기 위해 존재하는 예외 변수이다. 