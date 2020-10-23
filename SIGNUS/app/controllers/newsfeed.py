'''
SIGNUS newsfeed Controller
'''
from flask import current_app
from bson.json_util import dumps
from operator import itemgetter
from numpy import random
from app.models.mongodb.posts import Posts
from app.models.mongodb.category import Category


def newsfeed_recommendation(mongo_cur, user):
    '''
    추천 뉴스피드

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    user > 사용자 정보
    FT > FastText Module

    Return
    ---------
    뉴스피드 게시글 묶음 (List)
    '''
    posts_model = Posts(mongo_cur)
    category_model = Category(mongo_cur)
    
    FT = current_app.config["FT"]

    # 사용자 관심사 순 카테고리 정렬
    category_list = category_model.find_many(current_app.config["INDICATORS"]["CATEGORY_SET"])
    category_vector = []
    for category in category_list:
        vec = FT.vec_sim(user['topic_vector'], category['topic_vector'])
        category_vector += [(category['category_name'], vec, category['info_num'])]
    category_vector = sorted(category_vector, key=itemgetter(1), reverse=True)

    # 사용자 관심사 순 POST 불러오기
    POSTS_LIST = []
    POST_WEIGHT = current_app.config["INDICATORS"]["RECOM_POST_WEIGHT"]
    MINUS_WEIGHT = current_app.config["INDICATORS"]["RECOM_POST_MINUS_WEIGHT"]
    for category in category_vector:
        POSTS = posts_model.find_category_posts(category[2],
                                                current_app.config["INDICATORS"]["DEFAULT_DATE"],
                                                current_app.config["INDICATORS"]["GET_NF_POST_NUM"] + POST_WEIGHT)
        POSTS_LIST += [POSTS]
        POST_WEIGHT += MINUS_WEIGHT
    
    # Similarity 구하기
    for idx, posts in enumerate(POSTS_LIST):
        for post in posts:
            FAS = FT.vec_sim(user['topic_vector'], post['topic_vector']) * \
                  current_app.config["INDICATORS"]["FAS_WEIGHT"]
            IS = post['popularity'] / 120 * \
                 current_app.config["INDICATORS"]["IS_WEIGHT"]
            if IS > 1:
                IS = 1
            RANDOM = random.random() * \
                     current_app.config["INDICATORS"]["RANDOM_WEIGHT"]
            post['similarity'] = FAS + IS + RANDOM
        POSTS_LIST[idx] = sorted(POSTS_LIST[idx],
                                 key=itemgetter('similarity'),
                                 reverse=True)
    for idx, _ in enumerate(POSTS_LIST):
        POSTS_LIST[idx] = POSTS_LIST[idx][:current_app.config["INDICATORS"]["POSTS_NUM_BY_CATEGORY"][idx]]
    
    return dumps(POSTS_LIST[:current_app.config["INDICATORS"]["RETURN_NUM"]])


def newsfeed_popularity(mongo_cur):
    '''
    인기 뉴스피드

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object

    Return
    ---------
    뉴스피드 게시글 묶음 (List)
    '''
    posts_model = Posts(mongo_cur)
    return dumps(posts_model.find_popularity_posts(current_app.config["INDICATORS"]["DEFAULT_DATE"],
                                                   current_app.config["INDICATORS"]["RETURN_NUM"]))


def newsfeed_categroy(mongo_cur, category_name):
    '''
    카테고리 뉴스피드

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    category_name > 카테고리 이름

    Return
    ---------
    뉴스피드 게시글 묶음 (List)
    '''
    category_model = Category(mongo_cur)
    posts_model = Posts(mongo_cur)

    category = category_model.find_one(category_name)
    
    if category_name == "진로-구인":
        col = mongo_cur[current_app.config['MONGODB_DB_NAME']]['post_info']
        info = col.find_one({'info_id': 'sig48_vms_volunteer'})
        category['info_num'].remove(info['info_num'])

        vms_posts = posts_model.find_category_posts([info['info_num']],
                                                    current_app.config["INDICATORS"]["DEFAULT_DATE"],
                                                    40)
        normal_posts = posts_model.find_category_posts(category['info_num'],
                                                       current_app.config["INDICATORS"]["DEFAULT_DATE"],
                                                       210)
        
        result = vms_posts + normal_posts
        for post in result:
            post['similarity'] = RANDOM = random.random()
        result = sorted(result, key=itemgetter('similarity'), reverse=True)
        return dumps(result)

    return dumps(posts_model.find_category_posts(category['info_num'],
                                                 current_app.config["INDICATORS"]["DEFAULT_DATE"],
                                                 current_app.config["INDICATORS"]["GET_NF_POST_NUM"]))
