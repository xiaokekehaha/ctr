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

def get_week(seconds):
	temp = time.localtime(int(seconds))
	week = time.strftime('%U', temp)
	return week
#print get_date_diff('1428888880')
#print get_seconds('20150623')

