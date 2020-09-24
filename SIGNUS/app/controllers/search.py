'''
Search Controller Module
'''
from app.models.mongodb.posts import Posts


def search(mongo_cur, keyword, skip, limit, order):
    '''
    Search (검색)

    Params
    ---------
    mongo_cur > 몽고디비 커넥션 Object
    keyword > 검색 키워드
    skip > Document num skip
    limit > Document num limit
    order > sort order

    Return
    ---------
    posts > 포스트 (list)
    '''
    
    return []
