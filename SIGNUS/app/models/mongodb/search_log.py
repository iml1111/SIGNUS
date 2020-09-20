#SJ_DB_SEARCH_LOG 관련#################################
######################################################
#search_log에 search_obj 추가 (사용)
def insert_search_log(db, user_id, split_list):
	db[SJ_DB_SEARCH_LOG].insert(
		{
			'user_id': user_id,
			'search_split': split_list,
			'date': datetime.now()
		}
	)
	return "success"

#search_log 가져온다. (사용)
def find_search_log(db):
	result = db[SJ_DB_SEARCH_LOG].find(
		{
			'date':
			{
				'$gt': global_func.get_default_day(1)
			}
		},
		{
			'_id': 0,
			'search_split': 1
		}
	).sort([('date', -1)])

	return result

#총 검색 횟수 반환.
def find_search_count(db):
	result = db[SJ_DB_SEARCH_LOG].find().count()

	return result



