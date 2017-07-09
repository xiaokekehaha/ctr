#!usr/bin/python
import sys
sys.path.append('./')
import extract_feature
import time_stamp

last_user = ''
cur_user = ''

start_date = ['20150101', '20150115', '20150129', '20150212', '20150226', 
			  '20150312', '20150326', '20150409', '20150423', '20150526']
end_date   = ['20150129', '20150212', '20150226', '20150312', '20150326', 
              '20150409', '20150423', '20150507', '20150521', '20150623']
start_time = [0] * 10
for i in range(len(start_date)):
	start_time[i] = time_stamp.get_seconds(start_date[i])
end_time = [0] * 10
for i in range(len(end_date)):
	end_time[i] = time_stamp.get_seconds(end_date[i])

train_sets = {}
for i in range(10):
	train_sets[i] = []

for line in sys.stdin:
	line = line.strip()
	arr = line.split('\t')
	cur_user = arr[0]
	record = arr[1]
	arr = record.split(',')
	time = int(arr[7])
	if cur_user != last_user and last_user != '':
		for i in range(10):
			if len(train_sets[i]) > 0:
				print str(i) + '#' + extract_feature.extract_for_one_user(train_sets[i], end_time[i])
			train_sets[i] = []
	for i in range(10):
		if time >= start_time[i] and time <= end_time[i]:
			train_sets[i].append(record)
	last_user = cur_user

for i in range(10):
	if len(train_sets[i]) > 0:
		print str(i) + '#' + extract_feature.extract_for_one_user(train_sets[i], end_time[i])
