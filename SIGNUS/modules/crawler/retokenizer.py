import os
from modules.tokenizer import Tokenizer
from modules.recommender.fasttext import Recommender
from modules.crawler.list.url_list import List
from modules.crawler.dbs.mongo.db_connect import connect_db, disconnect_db

# Tokenizer 클래스 선언
TK = Tokenizer()

# FT (Recommender) 클래스 선언
FT = Recommender(os.getenv("SIGNUS_FT_MODEL_PATH"))


#모델링 함수
def retokenizer(db):
	for url in List:
		each_url_posts = list(db.posts.find(
			{"info":url["info"]})
			)
		for post_one in each_url_posts:
			if post_one["title"][-3:] == "..." and post_one["post"].startswith(post_one["title"][:-3]):
				post_one["title_token"] = post_one["post"][:20].split(" ")
			else:
				post_one["title_token"] = post_one["title"].split(" ")
			if post_one["post"].startswith(post_one["title"][:-3]):
				post_one["token"] = TK.get_tk(post_one["post"].lower())
			else:
				post_one["token"] = TK.get_tk(post_one["title"].lower() + post_one["post"].lower())
			post_one["token"] = list(url['title_tag'] + post_one["token"])

			if 'token' in post_one:
				topic_str = post_one["token"]
			else:
				topic_str = []
			post_one["topic_vector"] = FT.doc2vec(topic_str).tolist()
			db.posts.update_one(
				{'_id':post_one['_id']},
				{"$set":{

					"title_token":post_one["title_token"],
					"token":post_one["token"],
					"topic_vector":post_one["topic_vector"]
					}
				}
			)

if __name__ == '__main__':
	database = connect_db()
	db = database[1]
	retokenizer(db)