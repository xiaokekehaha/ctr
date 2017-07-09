import sys
sys.path.append('./')
import time_stamp
import my_format

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
def extract_for_one_user(input_list, end_time):
	#initial
	all_click_num = 0
	all_exposure_num = 0
	click_spid_set = set()
	exposure_spid_set = set()
	click_day_set = set()
	exposure_day_set = set()
	click = [0] * 5
	exposure = [0] * 5
	last_click_time = 30
	last_exposure_time = 30

	click_caid_set = set()
	exposure_caid_set = set()

	spid_click_dict = {}
	
	click_week = [0] * 5
	exposure_week = [0] * 5

	first_click_time = 0
	first_exposure_time = 0
	
	click_5days = [0] * 5
	exposure_5days = [0] * 5

	click_week_set = set()
	exposure_week_set = set()
	user_id = input_list[0].split(',')[0]

	click_day_diff = set()
	exposure_day_diff = set()
	#process all the data
	for data in input_list:
		arr = data.split(',')
		caid = arr[2]
		spid = arr[3]
		date = time_stamp.get_date(arr[7])
		day_diff = time_stamp.get_date_diff(arr[7], end_time)
		week = time_stamp.get_week(arr[7])
		if arr[8] == '1':
			all_click_num = all_click_num + 1
			click_spid_set.add(spid)
			click_day_set.add(date)
			last_click_time = min(last_click_time, day_diff)
			add_cnt(click, click_week, day_diff)
			click_caid_set.add(caid)
			if spid not in spid_click_dict:
				spid_click_dict[spid] = 0
			spid_click_dict[spid] = spid_click_dict[spid] + 1
			first_click_time = max(first_click_time, day_diff)
			if day_diff < 5:
				click_5days[day_diff] = click_5days[day_diff] + 1
			click_week_set.add(week)
			click_day_diff.add(day_diff)
		else:
			all_exposure_num = all_exposure_num + 1
			exposure_spid_set.add(spid)
			exposure_day_set.add(date)
			last_exposure_time = min(last_exposure_time, day_diff)
			add_cnt(exposure, exposure_week, day_diff)
			exposure_caid_set.add(caid)
			first_exposure_time = max(first_exposure_time, day_diff)
			if day_diff < 5:
				exposure_5days[day_diff] = exposure_5days[day_diff] + 1
			exposure_week_set.add(week)
			exposure_day_diff.add(day_diff)
	#print the feature set
	user_str = user_id
	
	all_exposure_num = all_exposure_num + all_click_num
	user_str = user_str + ' 1:' + str(all_exposure_num)
	if all_click_num > 0:
		user_str = user_str + ' 2:' + str(all_click_num)
		user_str = user_str + ' 3:' + my_format.string_cf(all_click_num, all_exposure_num)
	
	for i in range(len(click)):
		if click[i] > 0:
			user_str = user_str + ' ' + str(4 + i) + ':' + str(click[i])
	for i in range(len(exposure)):
		if exposure[i] > 0:
			user_str = user_str + ' ' + str(9 + i) + ':' + str(exposure[i])	
	
	temp = len(click_spid_set) + len(exposure_spid_set)
	user_str = user_str + ' 14:' + str(temp)
	if len(click_spid_set) >0:
		user_str = user_str + ' 15:' + str(len(click_spid_set)) 
		user_str = user_str + ' 16:' + my_format.string_cf(len(click_spid_set), temp)	
	
	if len(click_day_set) > 0:
		user_str = user_str + ' 17:' + str(len(click_day_set))
	if len(exposure_day_set) > 0:
		user_str = user_str + ' 18:' + str(len(exposure_day_set))

	user_str = user_str + ' 19:' + str(last_click_time) + ' 20:' + str(last_exposure_time)
	
	temp = len(click_caid_set) + len(exposure_caid_set)
	user_str = user_str + ' 21:' + str(temp)
	if len(click_caid_set) >0:
		user_str = user_str + ' 22:' + str(len(click_caid_set)) 
		user_str = user_str + ' 23:' + my_format.string_cf(len(click_caid_set), temp)	
	
	if len(click_spid_set) > 0:
		user_str = user_str + ' 24:' + my_format.string_cf(all_click_num, len(click_spid_set))
	
	click_2times_cnt = 0
	click_2times_sum = 0
	for s in spid_click_dict:
		if spid_click_dict[s] > 1:
			click_2times_cnt = click_2times_cnt + 1
			click_2times_sum = click_2times_sum + spid_click_dict[s]
	if click_2times_cnt > 0:
		user_str = user_str + ' 25:' + str(click_2times_sum) + ' 26:' + str(click_2times_cnt) + ' 27:' + my_format.string_cf(click_2times_sum, click_2times_cnt)
	for i in range(len(click_week)):
		if click_week[i] > 0:
			user_str = user_str + ' ' + str(28 + i) + ':' + str(click_week[i])
	for i in range(len(exposure_week)):
		if exposure_week[i] > 0:
			user_str = user_str + ' ' + str(33 + i) + ':' + str(exposure_week[i])	
	for i in range(len(exposure_week)):
		if click_week[i] > 0:
			user_str = user_str + ' ' + str(38 + i) + ':' + my_format.string_cf(click_week[i], click_week[i] + exposure_week[i])
	if first_click_time == 0:
		first_click_time = 30
	if first_exposure_time == 0:
		first_exposure_time = 30
	user_str = user_str + ' 43:' + str(first_click_time) + ' 44:' + str(first_exposure_time)
	
	click_5days_cnt = 0
	for i in range(len(click_5days)):
		if click_5days[i] > 0:
			user_str = user_str + ' ' + str(45 + i) + ':' + str(click_5days[i])
			click_5days_cnt = click_5days_cnt + click_5days[i]
	exposure_5days_cnt = 0
	for i in range(len(exposure_5days)):
		if exposure_5days[i] > 0:
			user_str = user_str + ' ' + str(50 + i) + ':' + str(exposure_5days[i])
			exposure_5days_cnt = exposure_5days_cnt + exposure_5days[i]
	for i in range(len(click_5days)):
		if click_5days[i] > 0:
			user_str = user_str + ' ' + str(55 + i) + ':' + my_format.string_cf(click_5days[i], click_5days[i] + exposure_5days[i])
	if click_5days_cnt > 0:
		user_str = user_str + ' 60:' + my_format.string_cf(click_5days_cnt, all_click_num)
	if exposure_5days_cnt > 0:
		user_str = user_str + ' 61:' + my_format.string_cf(exposure_5days_cnt, all_exposure_num)
	
	if click_2times_cnt > 0:
		user_str = user_str + ' 62:' + my_format.string_cf(click_2times_cnt, len(click_spid_set))
	if len(click_week_set) > 0:
		user_str = user_str + ' 63:' + str(len(click_week_set))
	if len(exposure_week_set) > 0:
		user_str = user_str + ' 64:' + str(len(exposure_week_set))
	day_diff_sum = 0
	for day_diff in click_day_diff:
		day_diff_sum = day_diff_sum + day_diff
	if day_diff_sum > 0:
		user_str = user_str + ' 65:' + my_format.string_cf(day_diff_sum, len(click_day_diff))
	day_diff_sum = 0
	for day_diff in exposure_day_diff:
		day_diff_sum = day_diff_sum + day_diff
	if day_diff_sum > 0:
		user_str = user_str + ' 66:' + my_format.string_cf(day_diff_sum, len(exposure_day_diff))

	return user_str
