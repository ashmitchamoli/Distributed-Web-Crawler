#!/usr/bin/env python3
# -*-coding:utf-8 -*

import sys

for line in sys.stdin:
    line = line.strip()
    key, neighbor = line.split()
    print(f"{key}\t{neighbor}")