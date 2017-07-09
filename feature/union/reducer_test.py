import sys
import random
sys.path.append('./')
import time_stamp
import extract_feature

user_ctr_dict = {}
user_feature = {}
for line in open('feature_user_9'):
	line = line.strip()
	idx = line.index(' ')
	user = line[2 : idx]
	user_feature[user] = line[idx + 1 :]
	if ' 3:' in line:
		idx = line.index(' 3:')
		line = line[idx + 3:]
		idx = line.index(' ')
		user_ctr_dict[user] = float(line[:idx])

spid_ctr_dict = {}
spid_feature = {}
for line in open('feature_spid_9'):
	line = line.strip()
	idx = line.index(' ')
	spid = line[2 : idx]
	spid_feature[spid] = line[idx + 1 :]
	if ' 69:' in line:
		idx = line.index(' 69:')
		line = line[idx + 4:]
		idx = line.index(' ')
		spid_ctr_dict[spid] = float(line[:idx])

caid_feature = {}
for line in open('feature_caid_9'):
	line = line.strip()
	idx = line.index(' ')
	caid = line[2 : idx]
	caid_feature[caid] = line[idx + 1 :]

browser_feature = {}
for line in open('feature_browser_9'):
	line = line.strip()
	idx = line.index(' ') 
	user = line[2 : idx]
	browser_feature[user] = line[idx + 1 :]

begin_time = time_stamp.get_seconds(sys.argv[1])
end_time = time_stamp.get_seconds(sys.argv[2])
test_end_time = time_stamp.get_seconds(sys.argv[3])
last_user = ''
cur_user = ''
user_list = []

for line in sys.stdin:
	line = line.strip()
	arr = line.split('\t')
	cur_user = arr[0]
	temp = arr[1]
	arr = temp.split(',')
	time = int(arr[7])
	if time < begin_time or time > test_end_time:
		continue
	if last_user != cur_user and last_user != '':
		user_ctr = 0
		if last_user in user_ctr_dict:
			user_ctr = user_ctr_dict[last_user]
		ans_list = extract_feature.extract_for_one_user(user_list, begin_time, end_time, test_end_time, user_ctr, spid_ctr_dict)
		for ans_str in ans_list:
			idx = ans_str.index(' ')
			label = ans_str[0 : idx].split('#')[0]
			caid = ans_str[0 : idx].split('#')[1]
			spid = ans_str[0 : idx].split('#')[2]	
			browser = ans_str[0 : idx].split('#')[3]
			label = last_user + "#" + spid +'#' + label
			interaction_feature = ans_str[idx + 1 :]
			print label + ' ' + user_feature[last_user] + ' ' + spid_feature[spid] + ' ' + caid_feature[caid] + ' ' + interaction_feature + ' ' + browser_feature[last_user + '#' + browser]
		user_list = []
	user_list.append(temp)
	last_user = cur_user

user_ctr = 0
if last_user in user_ctr_dict:
	user_ctr = user_ctr_dict[last_user]
ans_list = extract_feature.extract_for_one_user(user_list, begin_time, end_time, test_end_time, user_ctr, spid_ctr_dict)
for ans_str in ans_list:
	idx = ans_str.index(' ')
	label = ans_str[0 : idx].split('#')[0]
	caid = ans_str[0 : idx].split('#')[1]
	spid = ans_str[0 : idx].split('#')[2]	
	browser = ans_str[0 : idx].split('#')[3]
	label = last_user + "#" + spid +'#' + label
	interaction_feature = ans_str[idx + 1 :]
	print label + ' ' + user_feature[last_user] + ' ' + spid_feature[spid] + ' ' + caid_feature[caid] + ' ' + interaction_feature + ' ' + browser_feature[last_user + '#' + browser]
	
