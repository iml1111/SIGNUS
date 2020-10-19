from tqdm import tqdm
from datetime import datetime
import re
from datetime import datetime, timedelta

#실시간 검색어 함수 preprocess
def preprocess(doc):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags=re.UNICODE)
    doc = re.sub(r'\s+'," ", doc)
    doc = doc.lower()
    doc = re.sub(r'[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', doc)
    doc = emoji_pattern.sub(r'', doc)
    doc = re.compile('[^ ㄱ-ㅣ가-힣|a-z]+').sub('', doc)
    return doc

#실시간 검색어 추출 함수
def real_time_keywords(search_input):
    temp = [i['keyword_split'] for i in search_input]
    check_list = []
    for i in range(len(temp)):
        temp_word = []
        for j in range(len(temp[i])):
            temp[i][j] = preprocess(temp[i][j])
            if len(temp[i][j]) > 1: temp_word.append(temp[i][j])
        check_list.append(temp_word)
    
    result = {}
    for words in check_list:
        # 단일 단어 추가
        for i in range(len(words)):
            if words[i] in result: result[words[i]] += 1
            else: result[words[i]] = 1
        
        # 연속 단어 추가(정방향)
        for i in range(2,len(words)):
            key = " ".join(words[0:i+1])
            if key in result: result[key] += 1
            else: result[key] = 1

    result = sorted(result.items(), key = itemgetter(0))
    temp = []
    for i in range(len(result)-1):
        if ((result[i+1][0].startswith(result[i][0]) or result[i+1][0].endswith(result[i][0])) and result[i+1][1] >= result[i][1]): 
            continue
        temp.append(result[i])
    result = sorted(temp, key = lambda x: len(x[0]))   
    result = sorted(result, key = itemgetter(1), reverse = True)
    return result



def realtime(db, config):
    search_log_list = list(db['search_log'].find({
        'date': {'$gte': datetime.now() - timedelta(days = config.INDICATORS['REALTIME_EFFECTIVE_DAY'])}},
        {'_id': 0, 'keyword_split': 1}
    ))

    # 검색 로그 후보군 추출
    candidate_keywords = real_time_keywords(search_log_list)
    if len(candidate_keywords) == 0:
        return False
    
    # 비속어 필터링
    result_keywords = []
    for keyword in candidate_keywords:
        if (keyword in config.INDICATORS['BAD_LANGUAGE'] or
            len(keyword) > config.INDICATORS['REALTIME_KEYWORD_LEN']):
            continue
        result_keywords.append(keyword)
    
    # 후보군 실시간 검색어 개수가 "REALTIME_KEYWORD_LEN" 보다 적으면,
    # 가장 최신 실시간 검색어 리스트를 가져와 결합.
    if len(result_keywords) < config.INDICATORS['REALTIME_KEYWORD_LEN']:
        latest_realtime = list(db['realtime'].find().sort([('date', -1)]).limit(1))[0]['realtime']

        result_keywords.sort(key=lambda x:x[1], reverse=True)
        latest_realtime.sort(key=lambda x:x[1], reverse=True)

        # 후보군 실시간 검색어 중 점수가 가장 작은 값 찾고, 0.1 점 감소
        min_value = result_keywords[-1][1]
        min_value -= 0.1

        # (현재 후보군 키워드 / 최근 실시간 검색어 키워드) 중 중복 키워드 찾기
        overlap_keyword = list(set(dict(result_keywords)) & set(dict(latest_realtime)))

        for keyword in latest_realtime:
            for overlap in overlap_keyword:
                if keyword[0] == overlap:
                    continue
            if len(result_keywords) == config.INDICATORS['REALTIME_KEYWORD_LEN']:
                break
            result_keywords.append([keyword[0], min_value])
        
    db['realtime'].insert_one({
        'realtime': result_keywords[:config.INDICATORS['REALTIME_KEYWORD_LEN']],
        'date': datetime.now()})

    return result_keywords
