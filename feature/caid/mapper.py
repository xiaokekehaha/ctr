import sys
sys.path.append('./')
import time_stamp

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

for line in sys.stdin:
	arr = line.strip().split(',')
	caid = arr[2]
	time = int(arr[7])
	for i in range(10):
		if time >= start_time[i] and time <= end_time[i]:
			print str(i) + '#' + caid + '\t' + line.strip()
