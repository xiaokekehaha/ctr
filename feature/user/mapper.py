#!usr/bin/python
import sys

for line in sys.stdin:
	arr = line.strip().split(',')
	user = arr[0]
	print user + '\t' + line.strip()
