#!/usr/bin/env python3
# -*-coding:utf-8 -*

import sys

current_key = None
neighbors_set = set()  # Use a set to store unique neighbors

def emit_adjacency_list(key, neighbors_set):
    neighbors_str = '\t'.join(neighbors_set)
    print(f"{key}\t1\t{len(neighbors_set)}\t{neighbors_str}")

for line in sys.stdin:
    line = line.strip()
    key, neighbor = line.split('\t', 1)
    if current_key == key:
        neighbors_set.add(neighbor)  # Add neighbor to the set
    else:
        if current_key:
            emit_adjacency_list(current_key, neighbors_set)
        current_key = key
        neighbors_set = {neighbor}  # Initialize a new set for the current key

if current_key:
    emit_adjacency_list(current_key, neighbors_set)
