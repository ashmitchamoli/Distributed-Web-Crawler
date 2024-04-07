#!/usr/bin/env python3
"""mapper.py"""

import sys

lines = sys.stdin.readlines()
numNodes = len(lines)

for line in lines:
    line = line.strip()
    if line == '': continue
    page, myPageRank, *neighbors = line.split()
    print(line) # carry forward the graph structure
    print(f'{page}\tnumNodes\t{numNodes}') # pass on the number of nodes
    if neighbors[0] == '0': # there are no outgoing links
        continue

    outPageRank = float(myPageRank) / int(neighbors[0])
    for neighbor in neighbors[1:]:
        print(f'{neighbor}\t{outPageRank}')
    
    numNodes += 1