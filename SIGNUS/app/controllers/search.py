'''
Search Controller Module
'''
import math
from bson.json_util import dumps
from flask import current_app
from app.models.mongodb.posts import Posts


def v1_search(mongo_cur, keywords, order, rank_filter=True):
    '''
    Search (검색)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    keywords > 검색 키워드
    skip > Document num skip
    limit > Document num limit
    order > sort order

    Return
    ---------
    posts > 포스트 (list)
    '''
    posts_model = Posts(mongo_cur)
    TK = current_app.config["TK"]
    
    # 후보군 선정
    keyword_split = keywords.lower().strip().split()
    keyword_tokens = list(set(TK.get_tk(keywords) + keyword_split))
    posts = posts_model.search_posts(keywords,
                                     keyword_tokens,
                                     current_app.config['INDICATORS']['GET_SC_POST_NUM'])

    # 유사도 측정
    set_keyword_tokens = set(keyword_tokens)
    for post in posts:
        post['score'] = 0

        # 각 영역별 매칭 유사도 평가 (현재 t_index가 없는 관계로 title_token, token 두개의 컬럼으로 진행함)
        weight = {'title_token': current_app.config['INDICATORS']['TITLE_WEIGHT'],
                  'token': current_app.config['INDICATORS']['TOKEN_WEIGHT']}
        for _type in ['title_token', 'token']:
            point = weight[_type]
            set_post_tokens = set(post[_type])
            post['score'] += match_score(set_keyword_tokens, set_post_tokens) * point

        # regex 매칭 최종 유사도 평가 (현재 regex_str이 없는 관계로 title을 기준으로 판단)
        point = current_app.config['INDICATORS']['REGEX_WEIGHT']
        if keywords in post['title']:
            post['score'] = (post['score'] * point) + 2

        # 반환 컬럼 정리
        del post['token']
        del post['title_token']

    # 최하위 랭킹 제거
    posts.sort(key=lambda t:(-t['score']))
    if (rank_filter is True and
        len(posts) != 0 and
        posts[0]['score'] != posts[-1]['score'] and
        posts[-1]['score'] <= current_app.config['INDICATORS']['LOWEST_RANK']):
        target = get_first_min(posts,
                               0,
                               len(posts)-1,
                               current_app.config['INDICATORS']['LOWEST_RANK'])
        posts = posts[:target]

    # 정렬 선택
    if order == 1:
        posts.sort(key=lambda x:x['date'], reverse=True)

    return {'posts': dumps(posts[:current_app.config['INDICATORS']['RETURN_NUM']]),
            'length': len(posts)}
             

def match_score(set_keyword_tokens, set_post_tokens):
    '''
    검색 유사도 평가 수식

    Params
    ---------
    set_keyword_tokens > 검색 키워드 토큰
    set_post_tokens > Post 토큰

    Return
    ---------
    결과 점수 (int)
    '''
    mc = len(set_keyword_tokens & set_post_tokens)
    if len(set_keyword_tokens) != 0:
        mr = mc / len(set_keyword_tokens)
    else:
        mr = mc / 1
    return mc * (1 + mr + math.floor(mr))


def get_first_min(data, s, e, target):
    '''
    최하위 탐지 (Binary search)

    Params
    ---------
    data > Post_list
    s > post 시작 idx
    e > post 끝 idx
    target > 최하위 랭크 점수

    Return
    ---------
    최하위 결과 index (int)
    '''
    if s > e: return None
    mid = (s + e) // 2
    if mid <= 0: return None
    if (data[mid-1]['score'] > target and 
        data[mid]['score'] <= target):
        return mid
    elif (data[mid-1]['score'] > target and 
        data[mid]['score'] > target):
        return get_first_min(data, mid+1, e, target)
    else:
        return get_first_min(data, s, mid-1, target)