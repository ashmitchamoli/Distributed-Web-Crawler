#!/usr/bin/env python3
# -*-coding:utf-8 -*

import sys

current_key = None
neighbors = []


def emit_adjacency_list(key, neighbors):
    neighbors_str = '\t'.join(neighbors)
    print(f"{key}\t1\t{len(neighbors)}\t{neighbors_str}")


for line in sys.stdin:
    line = line.strip()
    key, neighbor = line.split('\t', 1)
    if current_key == key:
        neighbors.append(neighbor)
    else:
        if current_key:
            emit_adjacency_list(current_key, neighbors)
        current_key = key
        neighbors = [neighbor]

if current_key:
    emit_adjacency_list(current_key, neighbors)
