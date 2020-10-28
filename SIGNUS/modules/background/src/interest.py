from tqdm import tqdm
from datetime import datetime


def interest(db, config):
    renewal_time = db['master_config'].find_one({"key": "updated_at"})['value']
    target_users = list(db['user'].find({'updated_at':{'$gt': renewal_time}}))
    categories = list(db['category'].find())
    now_date = datetime.now()

    for user in tqdm(target_users):
        if not user['fav_list'] and not user['view_list']:
            continue
        
        # 최근 400개 까지만 보존. (400개 이후는 관심도에 영향을 미치지 않다고 판단.)
        user['fav_list'] = user['fav_list'][:400]
        user['view_list'] = user['view_list'][:400]
        user['search_list'] = user['search_list'][:400]
        # user['newsfeed_list'] = user['newsfeed_list'][:400]

        fav_token = []
        view_token = []
        search_keywords = []

        for fav in user['fav_list']:
            fav_token += fav['token']

        for view in user['view_list']:
            view_token += view['token']
        
        for search in user['search_list']:
            search_keywords += search['keyword_tokens']
        
        # 취합
        assemble_doc = fav_token * config.INDICATORS["FAV_WEIGHT"] +\
                       view_token * config.INDICATORS["VIEW_WEIGHT"] +\
                       search_keywords * config.INDICATORS["SEARCH_WEIGHT"]
        
        # 토픽 벡터 구하기
        topic_vector = config.FT.doc2vec(assemble_doc).tolist()

        # 사용자 Cold Point 갱신
        cold_point = len(user['fav_list']) +\
                     len(user['view_list']) +\
                     len(user['search_list'])
        
        # 사용자 갱신
        db['user'].update_one(
            {'user_id': user['user_id']},
            {
                '$set':
                {
                    'fav_list': user['fav_list'],
                    'view_list': user['view_list'],
                    'search_list': user['search_list'],
                    'topic_vector': topic_vector,
                    'cold_point': cold_point,
                    'updated_at': now_date
                }
            }
        )

    db['master_config'].update_one({"key": "updated_at"}, {"$set": {"value": now_date}})

    return len(target_users)
