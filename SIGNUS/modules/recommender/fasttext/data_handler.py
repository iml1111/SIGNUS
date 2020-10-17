'''
SIGNUS FT Model 데이터 정제 및 로더 모듈
'''
import os
import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm
from modules.tokenizer import Tokenizer

MONGODB_URI = os.environ['SIGNUS_MONGODB_URI']

def data_refine(cur):
    train_data_list = []
    tokenizer = Tokenizer()
    col_names = [
        "hidden_post",
        "old_posts",
        "signus_posts"
    ]

    for col_name in col_names:
        docs = cur[col_name].find(
            {},
            {"_id": 0,"title": 1, "post": 1}
        )
        docs_len = cur[col_name].count()
        
        print("Col:", col_name)
        print("Total len:", docs_len)

        for doc in tqdm(docs):
            title = doc['title']
            post = doc['post']
            train_data = {
                "doc_str": title + post,
                "tokens": tokenizer.get_tk(title + post)
            }
            train_data_list.append(train_data)

    print("[IML] 총 코퍼스 수:", len(train_data_list))
    print("[IML] 정제된 데이터 삽입중...")
    cur['train_data'].delete_many({})
    cur['train_data'].insert_many(train_data_list)


def token_analy(cur):
    col = cur.train_data
    corpora = col.find()
    tokens = []

    for corpus in corpora:
        tokens += corpus['tokens']

    print("[IML] 토큰 총 개수:", len(tokens))
    s = pd.Series(tokens)
    result = s.value_counts()
    return result
    # result.iloc[0:50]


def data_loader():
    cli = MongoClient(MONGODB_URI)
    col = cli['SIGNUS_TRAIN']['train_data']
    data_list = list(col.find())
    train_data = []
    for data in data_list:
        train_data.append(data['tokens'])
    return train_data


if __name__ == '__main__':
    mongo_cli = MongoClient(MONGODB_URI)
    print(MONGODB_URI)
    cur = mongo_cli['SIGNUS_TRAIN']

    data_refine(cur)
    # result = token_analy(cur)