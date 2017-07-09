import sys
import random
sys.path.append('./')
import time_stamp
import my_format

def fun(dict1, spid, day_diff):
	if day_diff <= 6:
		dict1[0][spid] = dict1[0][spid] + 1
	elif day_diff <= 12:
		dict1[1][spid] = dict1[1][spid] + 1
	elif day_diff <= 18:
		dict1[2][spid] = dict1[2][spid] + 1
	elif day_diff <= 24:
		dict1[3][spid] = dict1[3][spid] + 1

def add_time_info(weekday_dict, hour_dict, halfh_dict, spid, time):
	weekday = time_stamp.get_weekday(time) #0-6 : 7
	hour = time_stamp.get_hour(time) #0-23 : 24
	halfh = time_stamp.get_half_hour(time) #0-47 : 48
	weekday_dict[spid][weekday] = weekday_dict[spid][weekday] + 1
	hour_dict[spid][hour] = hour_dict[spid][hour] + 1
	halfh_dict[spid][halfh] = halfh_dict[spid][halfh] + 1

def extract_for_one_user(input_list, begin_time, end_time, test_end_time, user_ctr, spid_ctr_dict):
	if len(input_list) == 0:
		return []
	click = {}
	exposure = {}
	last_click_time = {}
	last_exposure_time = {}
	user = input_list[0].split(',')[0]

	test_click_spid = set()#label is 1
	all_spid = set()
	spid_dict = {}#spid to caid
	
	click_week_dict = [{}, {}, {}, {}]#first week
	exposure_week_dict = [{}, {}, {}, {}]
	
	click_weekday_dict = {}
	click_hour_dict = {}
	click_halfh_dict = {}
	exposure_weekday_dict = {}
	exposure_hour_dict = {}
	exposure_halfh_dict = {}

	
	first_click_time = {}
	first_exposure_time = {}
	
	click_cnt = 0	
	exposure_cnt = 0

	max_time = 0
	max_click_seconds = {}
	max_exposure_seconds = {}
	
	click_five_days = [{},{},{},{},{}]
	exposure_five_days = [{},{},{},{},{}]
	
	click_day_set = {}
	exposure_day_set = {}
	click_week_set = {}
	exposure_week_set = {}
	
	caid_click = {}
	caid_exposure = {}

	spid_browser = {}

	for line in input_list:
		arr = line.split(',')
		caid = arr[2]
		spid = arr[3]
		browser = arr[4]
		time = int(arr[7])
		weekday = time_stamp.get_weekday(arr[7]) #0-6 : 7
		hour = time_stamp.get_hour(arr[7]) #0-23 : 24
		minute = time_stamp.get_half_hour(arr[7]) #0-47 : 48
		if time >= begin_time and time <= end_time:
			all_spid.add(spid)
			if spid not in spid_dict:
				spid_dict[spid] = caid
			if arr[8] == '1':
				click_cnt = click_cnt + 1
			else:
				exposure_cnt = exposure_cnt + 1
			if spid not in spid_browser:
				spid_browser[spid] = browser
		
		if time > end_time and time < test_end_time and arr[8] == '1':
			test_click_spid.add(spid)
		if caid not in caid_click:
			caid_click[caid] = 0
		if caid not in caid_exposure:
			caid_exposure[caid] = 0

	for spid in all_spid:
		click[spid] = 0
		exposure[spid] = 0
		last_click_time[spid] = 30
		last_exposure_time[spid] = 30
		for i in range(len(click_week_dict)):
			click_week_dict[i][spid] = 0
			exposure_week_dict[i][spid] = 0
		click_weekday_dict[spid] = [0] * 7
		exposure_weekday_dict[spid] = [0] * 7
		click_hour_dict[spid] = [0] * 24
		exposure_hour_dict[spid] = [0] * 24
		click_halfh_dict[spid] = [0] * 48
		exposure_halfh_dict[spid] = [0] * 48
		first_click_time[spid] = 0
		first_exposure_time[spid] = 0
		max_click_seconds[spid] = 0
		max_exposure_seconds[spid] = 0
		for i in range(len(click_five_days)):
			click_five_days[i][spid] = 0
			exposure_five_days[i][spid] = 0
		click_week_set[spid] = set()
		exposure_week_set[spid] = set()
		click_day_set[spid] = set()
		exposure_day_set[spid] = set()
	user_click_day_set = set()
	user_exposure_day_set = set()
	for line in input_list:
		arr = line.split(',')
		caid = arr[2]
		spid = arr[3]
		time = int(arr[7])
		max_time = max(time, max_time)
		day_diff = time_stamp.get_date_diff(arr[7], end_time)
		date = time_stamp.get_date(arr[7])
		week = time_stamp.get_week(arr[7])
		if time < begin_time or time > end_time:# during training period
			continue
		if arr[8] == '1':
			click[spid] = click[spid] + 1
			last_click_time[spid] = min(last_click_time[spid], day_diff)
			fun(click_week_dict, spid, day_diff)
			add_time_info(click_weekday_dict, click_hour_dict, click_halfh_dict, spid, arr[7])
			first_click_time[spid] = max(first_click_time[spid], day_diff)
			max_click_seconds[spid] = max(max_click_seconds[spid], time)	
			if day_diff < 5:
				click_five_days[day_diff][spid] = click_five_days[day_diff][spid] + 1
			click_day_set[spid].add(date)
			click_week_set[spid].add(week)
			user_click_day_set.add(date)
			caid_click[caid] = caid_click[caid] + 1
		else:
			exposure[spid] = exposure[spid] + 1
			last_exposure_time[spid] = min(last_exposure_time[spid], day_diff)
			fun(exposure_week_dict, spid, day_diff)
			add_time_info(exposure_weekday_dict, exposure_hour_dict, exposure_halfh_dict, spid, arr[7])
			first_exposure_time[spid] = max(first_exposure_time[spid], day_diff)
			max_exposure_seconds[spid] = max(max_exposure_seconds[spid], time)	
			if day_diff < 5:
				exposure_five_days[day_diff][spid] = exposure_five_days[day_diff][spid] + 1
			exposure_day_set[spid].add(date)
			exposure_week_set[spid].add(week)
			user_exposure_day_set.add(date)
			caid_exposure[caid] = caid_exposure[caid] + 1  
	
	click_sort = sorted(click.items(), key = lambda d : d[1], reverse = True)
	spid_click_sort = []
	for item in click_sort:
		spid_click_sort.append(item[0])
	exposure_sort = sorted(exposure.items(), key = lambda d : d[1], reverse = True)
	spid_exposure_sort = []
	for item in exposure_sort:
		spid_exposure_sort.append(item[0])

	user_spid_list = []
	for key in all_spid:
		label = "0#" + spid_dict[key] + '#' + key + '#' + spid_browser[key]
		if key in test_click_spid:
			label = "1#" + spid_dict[key] + '#' + key + '#' + spid_browser[key]
		#if label[0] == '0' and end_time < test_end_time and random.random() > 0.015: #randomly select if train
		#	continue
		temp_str = label
		if click[key] > 0:
			temp_str = temp_str + ' 147:' + str(click[key])
		if last_exposure_time[key] == 30 and last_click_time[key] != 30:
			last_exposure_time[key] = last_click_time[key]
		temp_str = temp_str + ' 148:' + str(click[key] + exposure[key]) + ' 149:' + str(last_click_time[key]) + ' 150:' + str(last_exposure_time[key])
		
		for i in range(len(click_week_dict)):
			if click_week_dict[i][key] > 0:
				temp_str = temp_str + ' ' + str(151 + i) + ':' + str(click_week_dict[i][key])
		for i in range(len(exposure_week_dict)):
			if exposure_week_dict[i][key] > 0:
				temp_str = temp_str + ' ' + str(155 + i) + ':' + str(exposure_week_dict[i][key])
		for i in range(len(click_week_dict)):
			if click_week_dict[i][key] > 0:
				temp_str = temp_str + ' ' + str(159 + i) + ':' + my_format.string_cf(click_week_dict[i][key], click_week_dict[i][key] + exposure_week_dict[i][key])
		
		spid = key
		for i in range(7):#0-7
			if click_weekday_dict[spid][i] > 0:
				temp_str = temp_str + ' ' + str(163 + i) + ':' + str(click_weekday_dict[spid][i])
		for i in range(7):#0-7
			if exposure_weekday_dict[spid][i] > 0:
				temp_str = temp_str + ' ' + str(170 + i) + ':' + str(exposure_weekday_dict[spid][i])
		for i in range(24):
			if click_hour_dict[spid][i] > 0:
				temp_str = temp_str + ' ' + str(177 + i) + ':' + str(click_hour_dict[spid][i])
		for i in range(24):
			if exposure_hour_dict[spid][i] > 0:
				temp_str = temp_str + ' ' + str(201 + i) + ':' + str(exposure_hour_dict[spid][i])
		for i in range(48):
			if click_halfh_dict[spid][i] > 0:
				temp_str = temp_str + ' ' + str(225 + i) + ':' + str(click_halfh_dict[spid][i])
		for i in range(48):
			if exposure_halfh_dict[spid][i] > 0:
				temp_str = temp_str + ' ' + str(273 + i) + ':' + str(exposure_halfh_dict[spid][i])
		if first_click_time[spid] == 0:
			first_click_time[spid] = 30
		if first_exposure_time[spid] == 0:
			first_click_time[spid] = first_click_time[spid]
		temp_str = temp_str + ' 321:' + str(first_click_time[spid]) + ' 322:' + str(first_exposure_time[spid])
		if user_ctr != 0:
			temp_str = temp_str + ' 323:' + str((click[spid] + exposure[spid]) * user_ctr)
		if spid in spid_ctr_dict:
			temp_str = temp_str + ' 324:' + str((click[spid] + exposure[spid]) * spid_ctr_dict[spid])
		if click[spid] != 0:
			temp_str = temp_str + ' 325:' + my_format.string_cf(click[spid], click_cnt)
		if exposure[spid] != 0:
			temp_str = temp_str + ' 326:' + my_format.string_cf(exposure[spid], exposure_cnt)
		if click[spid] > 0:
			temp_str = temp_str + ' 327:' + my_format.string_cf(click[spid], click[spid] + exposure[spid])
		if max_click_seconds[spid] > 0:
			temp_str = temp_str + ' 328:' + str(max_time - max_click_seconds[spid])
		if max_exposure_seconds[spid] > 0:
			temp_str = temp_str + ' 329:' + str(max_time - max_exposure_seconds[spid])
		click_5days = 0
		for i in range(len(click_five_days)):
			if click_five_days[i][key] > 0:
				temp_str = temp_str + ' ' + str(330 + i) + ':' + str(click_five_days[i][key])
				click_5days = click_5days + click_five_days[i][key]
		exposure_5days = 0
		for i in range(len(exposure_five_days)):
			if exposure_five_days[i][key] > 0:
				temp_str = temp_str + ' ' + str(335 + i) + ':' + str(exposure_five_days[i][key])
				exposure_5days = exposure_5days + exposure_five_days[i][key]
		if click_5days > 0:
			temp_str = temp_str + ' 340:' + my_format.string_cf(click_5days, click_cnt)
		if exposure_5days > 0:
			temp_str = temp_str + ' 341:' + my_format.string_cf(exposure_5days, exposure_cnt)
		
		if len(click_day_set[spid]) > 0:
			temp_str = temp_str + ' 342:' + str(len(click_day_set[spid]))
		if len(exposure_day_set[spid]) > 0:
			temp_str = temp_str + ' 343:' + str(len(exposure_day_set[spid]))
		if len(click_week_set[spid]) > 0:
			temp_str = temp_str + ' 344:' + str(len(click_week_set[spid]))
		if len(exposure_week_set[spid]) > 0:
			temp_str = temp_str + ' 345:' + str(len(exposure_week_set[spid]))
		if spid_click_sort.index(spid) < 100:
			temp_str = temp_str + ' 346:' + str(spid_click_sort.index(spid))
		if spid_exposure_sort.index(spid) < 100:
			temp_str = temp_str + ' 347:' + str(spid_exposure_sort.index(spid))
		if len(click_day_set[spid]) > 0:
			 temp_str = temp_str + ' 348:' + my_format.string_cf(len(click_day_set[spid]), len(user_click_day_set))
		if len(exposure_day_set[spid]) > 0:
			temp_str = temp_str + ' 349:' + my_format.string_cf(len(exposure_day_set[spid]), len(user_exposure_day_set))
		if click[spid] > 0 and caid_click[spid_dict[spid]]:
			temp_str = temp_str + ' 350:' + my_format.string_cf(click[spid], caid_click[spid_dict[spid]])
		if exposure[spid] > 0 and caid_exposure[spid_dict[spid]]:
			temp_str = temp_str + ' 351:' + my_format.string_cf(exposure[spid], caid_exposure[spid_dict[spid]])
		user_spid_list.append(temp_str)

	return user_spid_list
