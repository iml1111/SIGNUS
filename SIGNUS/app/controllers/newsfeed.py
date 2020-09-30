'''
SIGNUS newsfeed Controller
'''
from flask import current_app
from bson.json_util import dumps
from numpy import random
from app.models.mongodb.posts import Posts
from app.models.mongodb.category import Category


def newsfeed_recommendation(mongo_cur, user, FT):
    '''
    추천 뉴스피드

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object

    Return
    ---------
    POSTS_LIST > 뉴스피드 게시글 묶음
    '''
    Posts_model = Posts(mongo_cur)
    Category_model = Category(mongo_cur)

    # 사용자 관심사 순 카테고리 정렬
    category_list = Category_model.find_many()
    category_vector = []
    for category in category_list:
        vec = FT.vec_sim(user['topic_vector'], category['topic_vector'])
        category_vector += [(category['category_name'], vec, category['info_num'])]
    category_vector = sorted(category_vector, key=itemgetter(1), reverse=True)

    # 사용자 관심사 순 POST 불러오기
    POSTS_LIST = []
    POST_WEIGHT = current_app.config["INDICATORS"]["RECOMMENDATION"]["RECOM_POST_WEIGHT"]
    MINUS_WEIGHT = current_app.config["INDICATORS"]["RECOMMENDATION"]["RECOM_POST_MINUS_WEIGHT"]
    for category in category_vector:
        POSTS = Posts_model.find_recom_posts(category[2],
                                             current_app.config["INDICATORS"]["RECOMMENDATION"]["DEFAULT_DATE"],
                                             current_app.config["INDICATORS"]["RECOMMENDATION"]["RECOM_POST_NUM"] + POST_WEIGHT)
        POSTS_LIST += [POSTS]
        POST_WEIGHT += MINUS_WEIGHT
    
    # Similarity 구하기
    for idx, posts in enumerate(POSTS_LIST):
        for post in posts:
            FAS = FT.vec_sim(user['topic_vector'], post['topic_vector']) * \
                  current_app.config["INDICATORS"]["RECOMMENDATION"]["FAS_WEIGHT"]
            RANDOM = random.random() * \
                     current_app.config["INDICATORS"]["RECOMMENDATION"]["RANDOM_WEIGHT"]
            post['similarity'] = FAS + RANDOM
        POSTS_LIST[idx] = sorted(POSTS_LIST[idx],
                                 key=operator.itemgetter('similarity'),
                                 reverse=True)
    for idx, _ in enumerate(POSTS_LIST):
        POSTS_LIST[idx] = POSTS_LIST[idx][:current_app.config["INDICATORS"]["RECOMMENDATION"]["POSTS_NUM_BY_CATEGORY"][idx]]
    
    return POSTS_LIST


def newsfeed_popularity(mongo_cur):
    '''
    인기 뉴스피드

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object

    Return
    ---------
    POSTS_LIST > 뉴스피드 게시글 묶음
    '''
    Posts_model = Posts(mongo_cur)
    return dumps(Posts_model.find_popularity_posts(current_app.config["INDICATORS"]["RECOMMENDATION"]["DEFAULT_DATE"],
                                             current_app.config["INDICATORS"]["RECOMMENDATION"]["RECOM_POST_NUM"]))