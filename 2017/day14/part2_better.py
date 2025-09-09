import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from day10.part2 import hash_string

def part2():
    input = "nbysizxe"

    # Part 1
    # Hash rows, convert to binary
    # We will number connected occupied nodes e.g. the first connected nodes we see will be numbered 2
    # When encountering occupied nodes in a row, we will check if they are connected to left and above occupied nodes
    # Preferring the left neighbor, rename a connecte node to the same number of its neighbor.
    # We may find that two separate subgraphs are in fact connected as we moved down the rows
    # Keep a map of connected subgraphs
    num_subgraphs = 0
    num_occupied_nodes = 0
    prev_row = "0" * 128
    for row_idx in range(128):
        # Has row and convert to binary
        row_hash = hash_string(f"{input}-{row_idx}")
        row = bin(int(row_hash, 16))[2:].zfill(128)
        # Run through row and check for occupied nodes
        for col_idx, char in enumerate(row):
            if char != "0":
                # Occupied node, check if it's connected to left or above neighbor
                num_occupied_nodes += 1
                left_char = "0"
                if col_idx > 0:
                    left_char = row[col_idx - 1] 
                
                up_char = prev_row[col_idx]
                if left_char == "1" and up_char == "1":
                    # This node connects two previous unconnected subgraphs
                    # Decrement number of subgraphs
                    num_subgraphs -= 1
                elif left_char == "0" and up_char == "0":
                    # Not connected to existing subgraph
                    num_subgraphs += 1
        prev_row = row

    # Part 1     
    print(num_occupied_nodes)

    # Part 2
    print(num_subgraphs)

part2()