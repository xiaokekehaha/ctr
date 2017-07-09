import sys
import time
import datetime

def get_date(seconds):
	temp = time.localtime(int(seconds))
	date = time.strftime('%Y-%m-%d', temp)
	return date

def get_date_diff(second, end_time):
	seconds = 24 * 60 * 60
	return (end_time - int(second)) / seconds

def get_seconds(date):
	date_time = datetime.datetime(int(date[0 : 4]), int(date[4 : 6]), int(date[6 : 8]))
	return int(time.mktime(date_time.timetuple()))

#print get_date(1434988880)
#print get_date_diff('1434124800')
#print get_seconds('20150613')

