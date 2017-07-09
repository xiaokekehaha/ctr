import sys
sys.path.append('./')
import my_format
import time_stamp

def add_cnt(num, week, day_diff):
	#cumulative
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
	#every six days
	if day_diff <= 6:
		week[0] = week[0] + 1
	elif day_diff <= 12:
		week[1] = week[1] + 1
	elif day_diff <= 18:
		week[2] = week[2] + 1
	elif day_diff <= 24:
		week[3] = week[3] + 1
	else:
		week[4] = week[4] + 1

start_date = ['20150101', '20150115', '20150129', '20150212', '20150226', 
             '20150312', '20150326', '20150409', '20150423', '20150526']
end_date   = ['20150129', '20150212', '20150226', '20150312', '20150326', 
             '20150409', '20150423', '20150507', '20150521', '20150623']

last_spid = ''
cur_spid = ''

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
click_user_dict = {}
click_week = [0] * 5
exposure_week = [0] * 5
click_5days = [0] * 5
exposure_5days = [0] * 5

click_week_set = set()
exposure_week_set = set()

for line in sys.stdin:
	arr = line.strip().split('\t')
	cur_spid = arr[0]
	end_time = time_stamp.get_seconds(end_date[int(cur_spid[0])])
	arr = arr[1].split(',')
	user = arr[0]
	time = time_stamp.get_date(arr[7])
	day_diff = time_stamp.get_date_diff(arr[7], end_time)
	week = time_stamp.get_week(arr[7])	
	if cur_spid != last_spid and last_spid != '':
		#print the last_spid
		spid_str = last_spid
		
		all_exposure_num = all_click_num + all_exposure_num
		spid_str = spid_str + ' 67:' + str(all_exposure_num)
		if all_click_num > 0:
			spid_str = spid_str + ' 68:' + str(all_click_num) + ' 69:' + my_format.string_cf(all_click_num, all_exposure_num)

		for i in range(len(click)):
			if click[i] > 0:
				spid_str = spid_str + ' ' + str(70 + i) + ':' + str(click[i])
		for i in range(len(exposure)):
			if exposure[i] > 0:
				spid_str = spid_str + ' ' + str(75 + i) + ':' + str(exposure[i])
		
		temp = len(click_user_set) + len(exposure_user_set)
		spid_str = spid_str + ' 80:' + str(temp)
		if len(click_user_set) > 0:
			spid_str = spid_str + ' 81:' + str(len(click_user_set)) + ' 82:' + my_format.string_cf(len(click_user_set), temp)
		
		if len(click_day_set) > 0:
			spid_str = spid_str + ' 83:' + str(len(click_day_set)) + ' 84:' + my_format.string_cf(len(click_day_set), len(click_day_set) + len(exposure_day_set))
		if len(exposure_day_set) > 0:
			spid_str = spid_str + ' 85:' + str(len(exposure_day_set))

		spid_str = spid_str + ' 86:' + str(large_click_time) + ' 87:' + str(large_exposure_time)
		
		if len(click_user_set) > 0:
			spid_str = spid_str + ' 88:' + my_format.string_cf(all_click_num, len(click_user_set))
		
		click_2user_cnt = 0
		click_2user_sum = 0
		for s in click_user_dict:
			if click_user_dict[s] > 1:
				click_2user_cnt = click_2user_cnt + 1
				click_2user_sum = click_2user_sum + click_user_dict[s]
		if click_2user_cnt > 0:
			spid_str = spid_str + ' 89:' + str(click_2user_sum) + ' 90:' + str(click_2user_cnt) + ' 91:' + my_format.string_cf(click_2user_sum, click_2user_cnt) + ' 92:' + my_format.string_cf(click_2user_cnt, len(click_user_set))

		for i in range(len(click_week)):
			if click_week[i] > 0:
				spid_str = spid_str + ' ' + str(93 + i) + ':' + str(click_week[i])
		for i in range(len(exposure_week)):
			if exposure_week[i] > 0:
				spid_str = spid_str + ' ' + str(98 + i) + ':' + str(exposure_week[i])
		for i in range(len(exposure_week)):
			if click_week[i] > 0:
				spid_str = spid_str + ' ' + str(103 + i) + ':' + my_format.string_cf(click_week[i], click_week[i] + exposure_week[i])
		click_5days_cnt = 0
		for i in range(len(click_5days)):
			if click_5days[i] > 0:
				spid_str = spid_str + ' ' + str(108 + i) + ':' + str(click_5days[i])
				click_5days_cnt = click_5days_cnt + click_5days[i]
		exposure_5days_cnt = 0
		for i in range(len(exposure_5days)):
			if exposure_5days[i] > 0:
				spid_str = spid_str + ' ' + str(113 + i) + ':' + str(exposure_5days[i])
				exposure_5days_cnt = exposure_5days_cnt + exposure_5days[i]
		for i in range(len(click_5days)):
			if click_5days[i] > 0:
				spid_str = spid_str + ' ' + str(118 + i) + ':' + my_format.string_cf(click_5days[i], click_5days[i] + exposure_5days[i])
		if click_5days_cnt > 0:
			spid_str = spid_str + ' 123:' + my_format.string_cf(click_5days_cnt, all_click_num)
		if exposure_5days_cnt > 0:
			spid_str = spid_str + ' 124:' + my_format.string_cf(exposure_5days_cnt, all_exposure_num)
		
		if len(click_week_set) > 0:
			spid_str = spid_str + ' 125:' + str(len(click_week_set))
		if len(exposure_week_set) > 0:
			spid_str = spid_str + ' 126:' + str(len(exposure_week_set))
		print spid_str

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
		click_user_dict = {}
		click_week = [0] * 5
		exposure_week = [0] * 5
		click_5days = [0] * 5
		exposure_5days = [0] * 5
		click_week_set = set()
		exposure_week_set = set()
	if arr[8] == '1':
		all_click_num = all_click_num + 1
		click_user_set.add(user)
		click_day_set.add(time)
		large_click_time = min(large_click_time, end_time - int(arr[7]))
		add_cnt(click, click_week, day_diff)
		if user not in click_user_dict:
			click_user_dict[user] = 0
		click_user_dict[user] = click_user_dict[user] + 1
		if day_diff < 5:
			click_5days[day_diff] = click_5days[day_diff] + 1
		click_week_set.add(week)
	else:
		all_exposure_num = all_exposure_num +1
		exposure_user_set.add(user)
		exposure_day_set.add(time)
		large_exposure_time = min(large_exposure_time, end_time - int(arr[7]))
		add_cnt(exposure, exposure_week, day_diff)	
		if day_diff < 5:
			exposure_5days[day_diff] = exposure_5days[day_diff] + 1
		exposure_week_set.add(week)
	last_spid = cur_spid
	
#print the last_spid
spid_str = last_spid
	
all_exposure_num = all_click_num + all_exposure_num
spid_str = spid_str + ' 67:' + str(all_exposure_num)
if all_click_num > 0:
	spid_str = spid_str + ' 68:' + str(all_click_num) + ' 69:' + my_format.string_cf(all_click_num, all_exposure_num)

for i in range(len(click)):
	if click[i] > 0:
		spid_str = spid_str + ' ' + str(70 + i) + ':' + str(click[i])
for i in range(len(exposure)):
	if exposure[i] > 0:
		spid_str = spid_str + ' ' + str(75 + i) + ':' + str(exposure[i])
	
temp = len(click_user_set) + len(exposure_user_set)
spid_str = spid_str + ' 80:' + str(temp)
if len(click_user_set) > 0:
	spid_str = spid_str + ' 81:' + str(len(click_user_set)) + ' 82:' + my_format.string_cf(len(click_user_set), temp)

if len(click_day_set) > 0:
	spid_str = spid_str + ' 83:' + str(len(click_day_set)) + ' 84:' + my_format.string_cf(len(click_day_set), len(click_day_set) + len(exposure_day_set))
if len(exposure_day_set) > 0:
	spid_str = spid_str + ' 85:' + str(len(exposure_day_set))

spid_str = spid_str + ' 86:' + str(large_click_time) + ' 87:' + str(large_exposure_time)
		
if len(click_user_set) > 0:
	spid_str = spid_str + ' 88:' + my_format.string_cf(all_click_num, len(click_user_set))
	
click_2user_cnt = 0
click_2user_sum = 0
for s in click_user_dict:
	if click_user_dict[s] > 1:
		click_2user_cnt = click_2user_cnt + 1
		click_2user_sum = click_2user_sum + click_user_dict[s]
if click_2user_cnt > 0:
	spid_str = spid_str + ' 89:' + str(click_2user_sum) + ' 90:' + str(click_2user_cnt) + ' 91:' + my_format.string_cf(click_2user_sum, click_2user_cnt) + ' 92:' + my_format.string_cf(click_2user_cnt, len(click_user_set))

for i in range(len(click_week)):
	if click_week[i] > 0:
		spid_str = spid_str + ' ' + str(93 + i) + ':' + str(click_week[i])
for i in range(len(exposure_week)):
	if exposure_week[i] > 0:
		spid_str = spid_str + ' ' + str(98 + i) + ':' + str(exposure_week[i])
for i in range(len(exposure_week)):
	if click_week[i] > 0:
		spid_str = spid_str + ' ' + str(103 + i) + ':' + my_format.string_cf(click_week[i], click_week[i] + exposure_week[i])
click_5days_cnt = 0
for i in range(len(click_5days)):
	if click_5days[i] > 0:
		spid_str = spid_str + ' ' + str(108 + i) + ':' + str(click_5days[i])
		click_5days_cnt = click_5days_cnt + click_5days[i]
exposure_5days_cnt = 0
for i in range(len(exposure_5days)):
	if exposure_5days[i] > 0:
		spid_str = spid_str + ' ' + str(113 + i) + ':' + str(exposure_5days[i])
		exposure_5days_cnt = exposure_5days_cnt + exposure_5days[i]
for i in range(len(click_5days)):
	if click_5days[i] > 0:
		spid_str = spid_str + ' ' + str(118 + i) + ':' + my_format.string_cf(click_5days[i], click_5days[i] + exposure_5days[i])

if click_5days_cnt > 0:
	spid_str = spid_str + ' 123:' + my_format.string_cf(click_5days_cnt, all_click_num)
if exposure_5days_cnt > 0:
	spid_str = spid_str + ' 124:' + my_format.string_cf(exposure_5days_cnt, all_exposure_num)
if len(click_week_set) > 0:
	spid_str = spid_str + ' 125:' + str(len(click_week_set))
if len(exposure_week_set) > 0:
	spid_str = spid_str + ' 126:' + str(len(exposure_week_set))
print spid_str
