'''
MongoDB user Collection Model
'''
from flask import current_app


class User:
    """RAAS DB user Model"""
    def __init__(self, client):
        self.col = client[current_app.config['MONGODB_DB_NAME']]['user']

    def insert_one(self, user_obj):
        ''' 유저 추가 '''
        self.col.insert_one(user_obj)
        return True

    def find_one(self, user_id, projection):
        ''' 특정 유저 반환 '''
        return self.col.find_one(
            {"user_id": user_id},
            {"_id": 0}
        )

    def find_many(self, projection):
        ''' 모든 유저 반환 '''
        return list(self.col.find(
            {},
            projection
        ))
    
    def find_gt_updated_at(self, updated_time):
        ''' updated_time(관심도 측정 시간)보다 
            이후인 유저 반환 '''
        return list(self.col.find(
            {"updated_at": {"$gt": updated_time}},
            projection
        ))

    def update_one(self, user_id, update_object):
        ''' 특정 사용자의 정보를 update '''
        self.col.update_one(
            {"user_id": user_id},
            {"$set": update_object}
        )
        return True

    def remove_one(self, user_id):
        ''' 특정 유저 삭제 '''
        print("not yet")

'''
#유저 생성 (사용)
def insert_user(db, user_id, user_pw, user_nickname):
    topic_temp = numpy.ones(LDA.NUM_TOPICS)
    topic = (topic_temp / topic_temp.sum()).tolist()

    user_nickname_tag = str(int(hashlib.sha256(user_id.encode('utf-8')).hexdigest(), 16) % 10**5)
    ft_vector = (numpy.zeros(FastText.VEC_SIZE)).tolist()
    tag = {}
    tag_sum = 1
    tag_vector = (numpy.zeros(FastText.VEC_SIZE)).tolist()
    fav_list = []
    view_list = []
    newsfeed_list = []
    search_list = []
    auto_login = 1
    renewal = datetime.now()
    privacy = 0
    measurement_num = 0
    authorize = 0
    student_id_hash = None

    result = db[SJ_DB_USER].insert(
        {
            'user_id': user_id,
            'user_pw': user_pw,
            'user_nickname': user_nickname + "#" + user_nickname_tag,
            'ft_vector': ft_vector,
            'tag': tag,
            'tag_sum': tag_sum,
            'tag_vector': tag_vector,
            'topic': topic,
            'fav_list': fav_list,
            'view_list': view_list,
            'newsfeed_list': newsfeed_list,
            'search_list': search_list,
            'auto_login': auto_login,
            'renewal': renewal,
            'privacy': privacy,
            'measurement_num': measurement_num,
            'authorize': authorize,
            'student_id_hash': student_id_hash
        })

    return "success"

#유저 관심도 초기화 (사용)
def update_user_measurement_reset(db, user_id):
    topic_temp = numpy.ones(LDA.NUM_TOPICS)
    topic = (topic_temp / topic_temp.sum()).tolist()

    ft_vector = (numpy.zeros(FastText.VEC_SIZE)).tolist()
    tag = {}
    tag_sum = 1
    tag_vector = (numpy.zeros(FastText.VEC_SIZE)).tolist()
    fav_list = []
    view_list = []
    newsfeed_list = []
    search_list = []
    renewal = datetime.now()
    measurement_num = 0

    db[SJ_DB_USER].update(
        {
            'user_id': user_id
        },
        {
            '$set':
            {
                'ft_vector': ft_vector,
                'tag': tag,
                'tag_sum': tag_sum,
                'tag_vector': tag_vector,
                'topic': topic,
                'fav_list': fav_list,
                'view_list': view_list,
                'newsfeed_list': newsfeed_list,
                'search_list': search_list,
                'renewal': renewal,
                'measurement_num': measurement_num
            }
        }
    )

    return "success"

#유저 갱신시간별 반환 (관심도 측정용) (사용)
def find_user_renewal(db, renewal_time):
    result = db[SJ_DB_USER].find(
        {	
            'renewal':
            {
                '$gt': renewal_time
            }
        }, 
        {
            'user_id': 1,
            'fav_list': 1,
            'view_list': 1,
            'search_list': 1,
            'newsfeed_list': 1,
            'measurement_num': 1
        }
    )
    return result

#유저 갱신 시간 갱신 (사용)
def update_user_renewal(db, user_id):
    db[SJ_DB_USER].update(
        {
            'user_id': user_id
        },
        {
            '$set':
            {
                'renewal': datetime.now()
            }
        }
    )
    return "success"

# ==============================================

#유저 fav_list 중복 체크 (사용)
def check_user_fav_list(db, _id, post_obi):
    result = db[SJ_DB_USER].find_one(
        {
            '_id': _id
        }, 
        {
            'fav_list': 
            {
                '$elemMatch': 
                {
                    '_id': post_obi
                }
            }
        }
    )
    return result

#유저 fav_list에 요소 추가 (사용)
def update_user_fav_list_push(db, _id, fav_obj):
    db[SJ_DB_USER].update(
        {
            '_id': _id
        },
        {
            '$push': 
            {
                'fav_list': 
                {
                    '$each': [fav_obj],
                    '$position': 0
                }
            }
        }
    )
    return "success"
#유저 fav_list에 요소 삭제 (사용)
def update_user_fav_list_pull(db, _id, post_obi):
    db[SJ_DB_USER].update(
        {
            '_id': _id
        },
        {
            '$pull': 
            {
                'fav_list': 
                {
                    '_id': post_obi
                }
            }
        }
    )
    return "success"

#유저 view_list에 요소 추가 (사용)
def update_user_view_list_push(db, _id, view_obj):
    db[SJ_DB_USER].update(
        {
            '_id': _id
        },
        {
            '$push': 
            {
                'view_list':
                {
                    '$each': [view_obj],
                    '$position': 0
                }
            }
        }
    )
    return "success"

#유저 search_list에 요소 추가 (사용)
def update_user_search_list_push(db, user_id, search_obj):
    db[SJ_DB_USER].update(
        {
            'user_id': user_id
        },
        {
            '$push': 
            {
                'search_list': 
                {
                    '$each': [search_obj],
                    '$position': 0
                }
            }
        }
    )
    return "success"

#유저 newsfeed_list에 요소 추가 (사용)
def update_user_newsfeed_list_push(db, _id, newsfeed_obj):
    db[SJ_DB_USER].update(
        {
            '_id': _id
        },
        {
            '$push': 
            {
                'newsfeed_list':
                {
                    '$each': [newsfeed_obj],
                    '$position': 0
                }
            }
        }
    )
    return "success"

#유저 관심도 갱신.
def update_user_measurement(db, _id, topic, tag, tag_sum, tag_vector, ft_vector, measurement_num):
    db[SJ_DB_USER].update({'_id': _id}, 
        {
            '$set': 
            {
                'topic': topic, 
                'tag': tag, 
                'tag_sum': tag_sum,
                'tag_vector': tag_vector,
                'ft_vector': ft_vector,
                'measurement_num': measurement_num
            }
        })

    return "success"

#유저 최근 검색 X개 불러오기
def find_user_lately_search(db, user_id, num):
    result = db[SJ_DB_USER].find_one(
        {	
            'user_id': user_id
        },
        {
            '_id': 0,
            'user_id': 0,
            'user_pw': 0,
            'user_nickname': 0,
            'ft_vector': 0,
            'topic': 0,
            'search_list': {'$slice': num},
            'fav_list': 0,
            'view_list': 0,
            'newsfeed_list': 0,
            'tag': 0,
            'tag_sum': 0,
            'auto_login': 0,
            'renewal': 0,
            'privacy': 0,
            'measurement_num': 0
        }
    )
    return result['search_list']

def update_user_action_log_refresh(db, _id, type_, refresh_obj):
    if type_ == "fav":
        #fav_list 삭제
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$unset': {'fav_list': 1}
            }
        )

        #새로운 fav_list 등록
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$push': 
                {
                    'fav_list':
                    {
                        '$each': refresh_obj,
                        '$position': 0
                    }
                }
            }
        )
    
    elif type_ == "view":
        #view_list 삭제
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$unset': {'view_list': 1}
            }
        )

        #새로운 view_list 등록
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$push': 
                {
                    'view_list':
                    {
                        '$each': refresh_obj,
                        '$position': 0
                    }
                }
            }
        )
    
    elif type_ == "search":
        #search_list 삭제
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$unset': {'search_list': 1}
            }
        )

        #새로운 search_list 등록
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$push': 
                {
                    'search_list':
                    {
                        '$each': refresh_obj,
                        '$position': 0
                    }
                }
            }
        )

    elif type_ == "newsfeed":
        #newsfeed_list 삭제
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$unset': {'newsfeed_list': 1}
            }
        )

        #새로운 newsfeed_list 등록
        db[SJ_DB_USER].update(
            {
                '_id': _id
            },
            {
                '$push': 
                {
                    'newsfeed_list':
                    {
                        '$each': refresh_obj,
                        '$position': 0
                    }
                }
            }
        )
    
    return "success"
'''