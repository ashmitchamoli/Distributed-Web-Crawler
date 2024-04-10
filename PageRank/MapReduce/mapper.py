#!/usr/bin/env python3
"""mapper.py"""

import sys

for line in sys.stdin.readlines():
    line = line.strip()
    if line == '': continue
    page, myPageRank, *neighbors = line.split()
    print(line) # carry forward the graph structure
    if neighbors[0] == '0': # there are no outgoing links
        continue

    outPageRank = float(myPageRank) / int(neighbors[0])
    for neighbor in neighbors[1:]:
        print(f'{neighbor}\t{outPageRank}')