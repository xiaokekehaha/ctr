import sys
sys.path.append('./')
import time_stamp

begin_time = time_stamp.get_seconds(sys.argv[1])
end_time = time_stamp.get_seconds(sys.argv[2])
for line in sys.stdin:
	arr = line.strip().split(',')
	time = int(arr[7])
	if time >= begin_time and time <= end_time:
		print arr[0] + '\t' + line.strip()
