#!/usr/bin/env python3
# -*-coding:utf-8 -*
import sys
for line in sys.stdin:
    line = line.strip().split()

    if line[1] not in {'0', '1'}:
        for k in line[1:]:
            print(line[0], k)
        print(line[0], 1)
    else:
        print(*line)
