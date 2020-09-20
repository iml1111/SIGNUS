#SJ_DB_POST 관련#######################################
######################################################
#포스트 전체 가져오기 (사용)
def find_all_posts(db, _id=None, title=None, date=None, end_date=None, post=None, tag=None, img=None, url=None, hashed=None, info=None, view=None, fav_cnt=None, title_token=None, token=None, topic=None, ft_vector=None, popularity=None, skip_=0, limit_=None):

	show_dict = {'_id': 0}

	if _id is not None:
		show_dict['_id'] = 1
	if title is not None:
		show_dict['title'] = 1
	if date is not None:
		show_dict['date'] = 1
	if end_date is not None:
		show_dict['end_date'] = 1
	if post is not None:
		show_dict['post'] = 1
	if tag is not None:
		show_dict['tag'] = 1
	if img is not None:
		show_dict['img'] = 1
	if url is not None:
		show_dict['url'] = 1
	if hashed is not None:
		show_dict['hashed'] = 1
	if info is not None:
		show_dict['info'] = 1
	if view is not None:
		show_dict['view'] = 1
	if fav_cnt is not None:
		show_dict['fav_cnt'] = 1
	if title_token is not None:
		show_dict['title_token'] = 1
	if token is not None:
		show_dict['token'] = 1
	if topic is not None:
		show_dict['topic'] = 1
	if ft_vector is not None:
		show_dict['ft_vector'] = 1
	if popularity is not None:
		show_dict['popularity'] = 1

	if limit_ is None:
		#기본적으로 날짜순 정렬 (최신)
		result = db[SJ_DB_POST].find(
			{}, 
			show_dict
		).sort([('date', -1)]).skip(skip_)

	else:
		#기본적으로 날짜순 정렬 (최신)
		result = db[SJ_DB_POST].find(
			{}, 
			show_dict
		).sort([('date', -1)]).skip(skip_).limit(limit_)

	return result

#포스트 단일 가져오기 (사용)
def find_post(db, post_obi, _id=None, title=None, date=None, end_date=None, post=None, tag=None, img=None, url=None, hashed=None, info=None, view=None, fav_cnt=None, title_token=None, token=None, topic=None, ft_vector=None, popularity=None):

	show_dict = {'_id': 0}

	if _id is not None:
		show_dict['_id'] = 1
	if title is not None:
		show_dict['title'] = 1
	if date is not None:
		show_dict['date'] = 1
	if end_date is not None:
		show_dict['end_date'] = 1
	if post is not None:
		show_dict['post'] = 1
	if tag is not None:
		show_dict['tag'] = 1
	if img is not None:
		show_dict['img'] = 1
	if url is not None:
		show_dict['url'] = 1
	if hashed is not None:
		show_dict['hashed'] = 1
	if info is not None:
		show_dict['info'] = 1
	if view is not None:
		show_dict['view'] = 1
	if fav_cnt is not None:
		show_dict['fav_cnt'] = 1
	if title_token is not None:
		show_dict['title_token'] = 1
	if token is not None:
		show_dict['token'] = 1
	if topic is not None:
		show_dict['topic'] = 1
	if ft_vector is not None:
		show_dict['ft_vector'] = 1
	if popularity is not None:
		show_dict['popularity'] = 1

	result = db[SJ_DB_POST].find_one(
		{
			'_id': ObjectId(post_obi)
		}, 
		show_dict
	)

	return result

#포스트 생성
def insert_post(db, title, post, tag, img, url, info, hashed, url_hashed, token, view, fav_cnt, title_token, login, learn, popularity, topic, ft_vector):
	db[SJ_DB_POST].insert(
		{
			'title': title,
			'post': post,
			'tag': tag,
			'img': img,
			'url': url,
			'info': info,
			'hashed': hashed,
			'url_hashed': url_hashed,
			'token': token,
			'view': view,
			'fav_cnt': fav_cnt,
			'title_token': title_token,
			'login': login,
			'learn': learn,
			'popularity': popularity,
			'topic': topic,
			'ft_vector': ft_vector,
			'date': datetime.now()
		}
	)

	return "success"

#포스트 수정
def update_post(db, post_obi, title, post, tag, img, url, info, hashed, url_hashed, token, title_token, topic, ft_vector):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		},
		{
			'$set':
			{
				'title': title,
				'post': post,
				'tag': tag,
				'img': img,
				'url': url,
				'info': info,
				'hashed': hashed,
				'url_hashed': url_hashed,
				'token': token,
				'title_token': title_token,
				'topic': topic,
				'ft_vector': ft_vector
			}
		}
	)

	return "success"

#포스트 삭제
def remove_post(db, post_obi):
	db[SJ_DB_POST].remove(
		{
			'_id': ObjectId(post_obi)
		}
	)
	return "success"

#포스트 좋아요 (사용)
def update_post_like(db, post_obi):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		}, 
		{
			'$inc': {'fav_cnt': 1, 'popularity': 3}
		}
	)
	return "success"

#포스트 좋아요 취소 (사용)
def update_post_unlike(db, post_obi):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		}, 
		{
			'$inc': 
			{
				'fav_cnt': -1, 
				'popularity': -3
			}
		}
	)
	return "success"

#포스트 조회수 올리기 (사용)
def update_post_view(db, post_obi):
	db[SJ_DB_POST].update(
		{
			'_id': ObjectId(post_obi)
		}, 
		{
			'$inc': 
			{
				'view': 1, 
				'popularity': 1
			}
		}
	)
	return "success"

#카테고리별 포스트들 반환 (사용)
def find_posts_of_category(db, info_num_list, now_date, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'info_num': {'$in': info_num_list}},
				{'end_date': {'$gt': now_date}}
			]
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'img': 1,
			'fav_cnt': 1,
			'view': 1,
			'url': 1,
			'title_token': 1,
			'info': 1,
			'tag': 1,
			'topic': 1,
			'ft_vector': 1,
			'end_date': 1
		}
	).sort([('date', -1)]).limit(num).hint("info_num_1_end_date_-1_date_-1")
	return result

#카테고리별 포스트들 반환 (디폴트 데이트도 적용된 쿼리) (사용)
def find_posts_of_category_default_date(db, info_num_list, now_date, default_date, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'info_num': {'$in': info_num_list}},
				{'end_date': {'$gt': now_date}},
				{'date': {'$gt': global_func.get_default_day(default_date)}}
			]
		},
		{
			'_id': 1,
            'title': 1,
            'date': 1,
            'img': 1,
            'fav_cnt': 1,
            #'view': 1,
            'url': 1,
            #'title_token': 1,
            #'info': 1,
            'tag': 1,
            'topic': 1,
            'ft_vector': 1,
            'end_date': 1,
            "popularity":1
		}
	).sort([('date', -1)]).limit(num).hint("info_num_1_end_date_-1_date_-1")
	return result

# 교내 공모전 : insideCampus
# 교외 공모전 : outsideCampus
# 데이터 개수 : limit
def find_posts_of_category_kiosk_1(db, num):
	result = db.posts.find(
		{
			"$and": 
			[ 
				{ "tag": "공모전&대외활동" },
				{ "tag": "교내"},         
			] 
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'img': 1,
			'fav_cnt': 1,
			'view': 1,
			'url': 1,
			'title_token': 1,
			'info': 1,
			'tag': 1,
			'topic': 1,
			'ft_vector': 1,
			'end_date': 1
		}
	).sort([('date', -1)]).limit(num)
	return result

def find_posts_of_category_kiosk_2(db, num):
	result = db.posts.find(
		{
			"$and": 
			[ 
				{ "tag": "공모전&대외활동" },
				{ "tag": {"$ne":"교내"} },          
			] 
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'img': 1,
			'fav_cnt': 1,
			'view': 1,
			'url': 1,
			'title_token': 1,
			'info': 1,
			'tag': 1,
			'topic': 1,
			'ft_vector': 1,
			'end_date': 1
		}
	).sort([('date', -1)]).limit(num)
	return result

#추천 뉴스피드 포스트들 불러오기 (미사용)
def find_posts_of_recommendation(db, now_date, num):
	result = db[SJ_DB_POST].find(
		{
			'end_date': {'$gt': now_date}
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'img': 1,
			'fav_cnt': 1,
			'view': 1,
			'url': 1,
			'title_token': 1,
			'info': 1,
			'tag': 1,
			'topic': 1,
			'ft_vector': 1,
			'end_date': 1
		}
	).sort([('date', -1)]).limit(num)
	return result

#인기 뉴스피드 반환 (사용)
def find_popularity_newsfeed(db, default_date, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'popularity': {'$gt': 0}},
				{'date': {'$gt': global_func.get_default_day(default_date)}}
			]
		},
		{
			'_id': 1,
			'title': 1,
			'date': 1,
			'end_date': 1,
			'img': 1,
			'fav_cnt': 1,
			'url': 1,
			'popularity': 1
		}
		).sort([('popularity', -1)]).limit(num)
	return result

#카테고리 검색 (디폴트 데이트도 적용된 쿼리) (사용)
def find_search_of_category(db, search_list, info_num_list, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'token': {'$in': search_list}},
				{'info_num': {'$in': info_num_list}}
			]
		},
		{
			'_id':1, 
			'title':1,
			'date':1,
			'end_date':1,
			'img': 1,
			'url': 1,
			'fav_cnt': 1,
			'info': 1,
			###############
			'title_token':1,
			'token':1,
			'tag':1,
			'popularity':1,
			'ft_vector': 1
		}
		).sort([('date', -1)]).limit(num)
	return result

#카테고리 검색 (디폴트 데이트도 적용된 쿼리) (사용)
def find_search_of_category_default_date(db, search_list, info_num_list, default_date, num):
	result = db[SJ_DB_POST].find(
		{
			'$and':
			[
				{'token': {'$in': search_list}},
				{'info_num': {'$in': info_num_list}},
				{'date': {'$gt': global_func.get_default_day(default_date)}}
			]
		},
		{
			'_id':1, 
			'title':1,
			'date':1,
			'end_date':1,
			'img': 1,
			'url': 1,
			'fav_cnt': 1,
			'info': 1,
			###############
			'title_token':1,
			'token':1,
			'tag':1,
			'popularity':1,
			'ft_vector': 1
		}
		).sort([('date', -1)]).limit(num)
	return result

#총 DB포스트 갯수 반환
def find_posts_count(db):
	result = db[SJ_DB_POST].find().count()

	return result

#제일 높은 좋아요 수 반환
def find_highest_fav_cnt(db):
	result = db[SJ_DB_POST].find(
		{},
		{
			'_id': 0,
			'fav_cnt': 1
		}
	).sort([('fav_cnt', -1)]).limit(1)
	return result[0]['fav_cnt']

#제일 높은 조회수 반환
def find_highest_view_cnt(db):
	result = db[SJ_DB_POST].find(
		{},
		{
			'_id': 0,
			'view': 1
		}
	).sort([('view', -1)]).limit(1)
	return result[0]['view']

#더미 포스트 체크(있는지 확인용)
def check_dummy_post(db):
	result = db[SJ_DB_POST].find_one({'title': "(o^_^)o 안녕하세요. SOOJLE 입니다."})

	return result

#좋아요/조회수 초기 셋팅용 더비 포스트 생성
def insert_dummy_post(db):
	topic_temp = numpy.ones(LDA.NUM_TOPICS)
	topic = (topic_temp / topic_temp.sum()).tolist()
	db[SJ_DB_POST].insert(
		{
			'title' : "(o^_^)o 안녕하세요. SOOJLE 입니다.",
			'date': global_func.get_default_day(10000),
			'post': "안녕하세요. SOOJLE 입니다.",
			'tag': [],
			'img': 1,
			'url': "",
			'hashed': "",
			'info': "SOOJLE",
			'view': 1,
			'fav_cnt': 1,
			'title_token': [],
			'token': [],
			'login': 0,
			'learn': 1,
			'popularity': 0,
			'fav_vector': (numpy.zeros(FastText.VEC_SIZE)).tolist(),
			'topic': topic
		}
	)
	return "success"
