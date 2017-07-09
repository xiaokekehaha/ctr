import sys
sys.path.append('./')
import my_format
import time_stamp

last_key = ''
click_num = 0
exposure_num = 0
click_day = set()
exposure_day = set()
for line in sys.stdin:
	arr = line.strip().split('\t')
	cur_key = arr[0]
	arr = arr[1].split(',')
	date = time_stamp.get_date(arr[7])
	if cur_key != last_key and last_key != '':
		browser_str = last_key
		if click_num > 0:
			browser_str = browser_str + ' 352:' + str(click_num)
			browser_str = browser_str + ' 353:' + my_format.string_cf(click_num, click_num + exposure_num)
		if exposure_num > 0:
			browser_str = browser_str + ' 354:' + str(exposure_num)
		if len(click_day) > 0:
			browser_str = browser_str + ' 355:' + str(len(click_day))
			browser_str = browser_str + ' 356:' + my_format.string_cf(len(click_day), len(click_day) + len(exposure_day))
		if len(exposure_day) > 0:
			browser_str = browser_str + ' 357:' + str(len(exposure_day))
		if ' ' in browser_str:
			print browser_str
		click_num = 0
		exposure_num = 0
		click_day = set()
		exposure_day = set()
	if arr[8] == '1':
		click_num = click_num + 1
		click_day.add(date)
	else:
		exposure_num = exposure_num + 1 
		exposure_day.add(date)
	last_key = cur_key

browser_str = last_key
if click_num > 0:
	browser_str = browser_str + ' 352:' + str(click_num)
	browser_str = browser_str + ' 353:' + my_format.string_cf(click_num, click_num + exposure_num)
if exposure_num > 0:
	browser_str = browser_str + ' 354:' + str(exposure_num)
if len(click_day) > 0:
	browser_str = browser_str + ' 355:' + str(len(click_day))
	browser_str = browser_str + ' 356:' + my_format.string_cf(len(click_day), len(click_day) + len(exposure_day))
if len(exposure_day) > 0:
	browser_str = browser_str + ' 357:' + str(len(exposure_day))
if ' ' in browser_str:
	print browser_str
		
