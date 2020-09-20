
#SJ_DB_CATEGORY 관련###################################
######################################################
#카테고리별 타입 전체 반환
def find_all_category_of_topic(db):
	result = db[SJ_DB_CATEGORY].find(
		{},
		{
			"tag":1,
			"category_name":1,
			"info_num":1,
			"tag_vector": 1
		}
	)
	return result

#카테고리별 타입 여러개 반환 (사용)
def find_category_of_topic_list(db, category_list):
	result = db[SJ_DB_CATEGORY].find(
			{
				'category_name': {'$in': category_list}
			}, 
			{
				"tag":1,
				"category_name":1,
				"info_num":1,
				"tag_vector": 1
			}
		)
	return result

#카테고리별 타입 반환 (사용)
def find_category_of_topic(db, category_name):
	result = db[SJ_DB_CATEGORY].find_one(
		{
			'category_name': category_name
		}, 
		{
			"tag":1,
			"category_name":1,
			"info_num":1,
			"tag_vector": 1
		}
	)
	return result

