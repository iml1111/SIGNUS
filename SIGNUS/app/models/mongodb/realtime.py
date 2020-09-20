
#SJ_DB_REALTIME 관련###################################
######################################################
#search_realtime 가져오기!
def find_search_all_realtime(db):
	result = db[SJ_DB_REALTIME].find(
		{},
		{
			'_id': 0
		}
	)
	return result

#search_realtime 단일 가져오기!
def find_search_realtime(db):
	result = db[SJ_DB_REALTIME].find(
		{},
		{
			'_id': 0,
			'real_time': 1,
			'date': 1
		}
	).sort([('date', -1)]).limit(1)
	return result

#search_realtime에 기록!
def insert_search_realtime(db, real_time_list):
	db[SJ_DB_REALTIME].insert(
		{
			'real_time' : real_time_list,
			'date': datetime.now()
		}
	)
	return "success"

