import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from day10.part2 import hash_string
from collections import deque

def part2():
    input = open('input.txt', 'r').readline()

    # Hash rows, convert to binary, and keep track of occupied nodes
    occupied_nodes = deque()
    for row_idx in range(128):
        row_hash = hash_string(f"{input}-{row_idx}")
        binary_hash = bin(int(row_hash, 16))[2:].zfill(128)
        for col_idx, char in enumerate(binary_hash):
            if char != "0":
                occupied_nodes.append((row_idx, col_idx))

    # Part 1 answer          
    print(len(occupied_nodes))

    # enumerate subgraphs
    num_subgraphs = 0
    while occupied_nodes:
        # Pop an unseen_node (a new subgraph member)
        # Visit the node's whole subgraph via BFS
        num_subgraphs += 1
        to_visit = deque([occupied_nodes[0]])
        while to_visit:
            (row_idx, col_idx) = to_visit.popleft()
            if (row_idx, col_idx) in occupied_nodes:
                occupied_nodes.remove((row_idx, col_idx))
                to_visit.append((row_idx - 1, col_idx))
                to_visit.append((row_idx + 1, col_idx))
                to_visit.append((row_idx, col_idx - 1))
                to_visit.append((row_idx, col_idx + 1))

    # Part 2 answer
    print(num_subgraphs)

part2()