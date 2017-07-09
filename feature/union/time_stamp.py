import sys
import time
import datetime

def get_date(seconds):
	temp = time.localtime(int(seconds))
	date = time.strftime('%Y-%m-%d', temp)
	return date

def get_week(seconds):
	temp = time.localtime(int(seconds))
	week = time.strftime('%U', temp)
	return week

def get_date_diff(second, end_time):
	seconds = 24 * 60 * 60
	return (end_time - int(second)) / seconds

def get_seconds(date):
	date_time = datetime.datetime(int(date[0 : 4]), int(date[4 : 6]), int(date[6 : 8]))
	return int(time.mktime(date_time.timetuple()))

def get_hour(seconds):
	temp = time.localtime(int(seconds))
	hour = int(time.strftime('%H', temp))
	minute = int(time.strftime('%M', temp))
	return hour

def get_weekday(seconds):
	temp = time.localtime(int(seconds))
	weekday = int(time.strftime('%w', temp))
	#if weekday == 0:
	#	weekday = 7
	return weekday

def get_half_hour(seconds):
	temp = time.localtime(int(seconds))
	hour = int(time.strftime('%H', temp))
	minute = int(time.strftime('%M', temp))
	return (hour * 2 + (minute / 30))

#print get_date(1434988880)
#print get_date_diff('1428888880')
#print get_seconds('20150623')
#print get_date('1275783299')
#print get_half_hour('1275783299')
