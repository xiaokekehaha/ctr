import sys

file_name = "" #user, spid, caid, browser
fs = []
for i in range(10):
	f = file('feature_' + file_name + '_' + str(i), 'w+')
	fs.append(f)

for line in sys.stdin:
	i = int(line[0])
	fs[i].write(line.strip() + '\n')

for i in range(10):
	fs[i].close()
