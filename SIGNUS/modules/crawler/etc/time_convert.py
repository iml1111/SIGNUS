import datetime


#str 타입을 datetime 타입으로 convert
def datetime_to_mongo(before_time):
	after_time = datetime.datetime.strptime(before_time, "%Y-%m-%d %H:%M:%S")

	return after_time

#datetime 타입을 str 타입으로 convert
def mongo_to_datetime(before_time):
	after_time = datetime.datetime.strftime(before_time, "%Y-%m-%d %H:%M:%S")

	return after_time