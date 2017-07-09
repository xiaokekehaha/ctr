import sys
sys.path.append('./')
import my_format
import time_stamp

def add_cnt(num, day_diff):
	if day_diff <= 5:
		num[0] = num[0] + 1
	if day_diff <= 10:
		num[1] = num[1] + 1
	if day_diff <= 15:
		num[2] = num[2] + 1
	if day_diff <= 20:
		num[3] = num[3] + 1																
	if day_diff <= 25:
		num[4] = num[4] + 1

#begin_time = time_stamp.get_seconds(sys.argv[1])
#end_time = time_stamp.get_seconds(sys.argv[2])
start_date = ['20150101', '20150115', '20150129', '20150212', '20150226', 
		      '20150312', '20150326', '20150409', '20150423', '20150526']
end_date   = ['20150129', '20150212', '20150226', '20150312', '20150326', 
		      '20150409', '20150423', '20150507', '20150521', '20150623']

last_caid = ''
cur_caid = ''
all_click_num = 0
all_exposure_num = 0
click_user_set = set()
exposure_user_set = set()
click_day_set = set()
exposure_day_set = set()
click = [0] * 5
exposure = [0] * 5
large_click_time = 999999999
large_exposure_time = 999999999

for line in sys.stdin:
	arr = line.strip().split('\t')
	cur_caid = arr[0]
	end_time = time_stamp.get_seconds(end_date[int(cur_caid[0])])
	arr = arr[1].split(',')
	user = arr[0]
	time = time_stamp.get_date(arr[7])
	day_diff = time_stamp.get_date_diff(arr[7], end_time)
	#if int(arr[7]) < begin_time or int(arr[7]) > end_time:
	#	continue
	if cur_caid != last_caid and last_caid != '':
		#print the last_caid
		caid_str = last_caid
		
		all_exposure_num = all_click_num + all_exposure_num
		caid_str = caid_str + ' 127:' + str(all_exposure_num)
		if all_click_num > 0:
			caid_str = caid_str + ' 128:' + str(all_click_num)
			caid_str = caid_str + ' 129:' + my_format.string_cf(all_click_num, all_exposure_num)

		for i in range(len(click)):
			if click[i] > 0:
				caid_str = caid_str + ' ' + str(130 + i) + ':' + str(click[i])
		for i in range(len(exposure)):
			if exposure[i] > 0:
				caid_str = caid_str + ' ' + str(135 + i) + ':' + str(exposure[i])
		
		temp = len(click_user_set) + len(exposure_user_set)
		caid_str = caid_str + ' 140:' + str(temp)
		if len(click_user_set) > 0:
			caid_str = caid_str + ' 141:' + str(len(click_user_set))
			caid_str = caid_str + ' 142:' + my_format.string_cf(len(click_user_set), temp)
		
		if len(click_day_set) > 0:
			caid_str = caid_str + ' 143:' + str(len(click_day_set))
		if len(exposure_day_set) > 0:
			caid_str = caid_str + ' 144:' + str(len(exposure_day_set))

		caid_str = caid_str + ' 145:' + str(large_click_time) + ' 146:' + str(large_exposure_time)
		print caid_str

		#clear all the statistics 
		all_click_num = 0
		all_exposure_num = 0
		click_user_set = set()
		exposure_user_set = set()
		click_day_set = set()
		exposure_day_set = set()
		click = [0] * 5
		exposure = [0] * 5
		large_click_time = 999999999
		large_exposure_time = 999999999
	if arr[8] == '1':
		all_click_num = all_click_num + 1
		click_user_set.add(user)
		click_day_set.add(time)
		large_click_time = min(large_click_time, end_time - int(arr[7]))
		add_cnt(click, day_diff)
	else:
		all_exposure_num = all_exposure_num + 1
		exposure_user_set.add(user)
		exposure_day_set.add(time)
		large_exposure_time = min(large_exposure_time, end_time - int(arr[7]))
		add_cnt(exposure, day_diff)	
	last_caid = cur_caid
	
#print the last_caid
caid_str = last_caid
		
all_exposure_num = all_click_num + all_exposure_num
caid_str = caid_str + ' 127:' + str(all_exposure_num)
if all_click_num > 0:
	caid_str = caid_str + ' 128:' + str(all_click_num)
	caid_str = caid_str + ' 129:' + my_format.string_cf(all_click_num, all_exposure_num)

for i in range(len(click)):
	if click[i] > 0:
		caid_str = caid_str + ' ' + str(130 + i) + ':' + str(click[i])
for i in range(len(exposure)):
	if exposure[i] > 0:
		caid_str = caid_str + ' ' + str(135 + i) + ':' + str(exposure[i])
		
temp = len(click_user_set) + len(exposure_user_set)
caid_str = caid_str + ' 140:' + str(temp)
if len(click_user_set) > 0:
	caid_str = caid_str + ' 141:' + str(len(click_user_set))
	caid_str = caid_str + ' 142:' + my_format.string_cf(len(click_user_set), temp)
		
if len(click_day_set) > 0:
	caid_str = caid_str + ' 143:' + str(len(click_day_set))
if len(exposure_day_set) > 0:
	caid_str = caid_str + ' 144:' + str(len(exposure_day_set))

caid_str = caid_str + ' 145:' + str(large_click_time) + ' 146:' + str(large_exposure_time)
print caid_str
