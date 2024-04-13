#!/usr/bin/env python3
# -*-coding:utf-8 -*
import sys

current_url = None
current_count = 0
state = False

for line in sys.stdin:
	line = line.strip().split()

	# this IF-switch only works because Hadoop sorts map output
	# by key (here: word) before it is passed to the reducer
	if line[1] in {'0', '1'}:
		if current_url == line[0]:
			state = state or bool(int(line[1]))
		else:
			if current_url:
				print(current_url, int(state))
			state = bool(int(line[1]))
			current_url = line[0]
	else:
		# print(line[0], 1)
		print(*line)
		current_url = None
		current_count = 0
		state = False
if current_url:
	print(current_url, int(state))

