from collections import deque

def main():
    example1_input_path = '/home/john/Documents/Projects/advent_of_code/2024/day12/input/example1.txt'
    example2_input_path = '/home/john/Documents/Projects/advent_of_code/2024/day12/input/example2.txt'
    example3_input_path = '/home/john/Documents/Projects/advent_of_code/2024/day12/input/example3.txt'
    example4_input_path = '/home/john/Documents/Projects/advent_of_code/2024/day12/input/example4.txt'
    example5_input_path = '/home/john/Documents/Projects/advent_of_code/2024/day12/input/example5.txt'
    part1_input_path = '/home/john/Documents/Projects/advent_of_code/2024/day12/input/input.txt'

    part2(example1_input_path) # Correct answer: Perimeter - 140,     Side - 80
    part2(example2_input_path) # Correct answer: Perimeter - 772,     Side - 436
    part2(example3_input_path) # Correct answer: Perimeter - 1930,    Side - NA
    part2(example4_input_path) # Correct answer: Perimeter - NA,      Side - 236
    part2(example5_input_path) # Correct answer: Perimeter - NA,      Side - 368
    part2(part1_input_path)    # Correct answer: Perimeter - 1457298, Side - 921636

def part2(input_path):
    # Input is essentially a graph with many subgraphs
    # Non-contiguous subgraphs may have the same letter, but should be treated separately
    # E.g. there may be two 'A' subgraphs that are not connected. They should be treated individually
    # BFS search to visit unseen nodes and traverse their subgraphs 
    input = open(input_path, 'r').readlines()
    num_rows = len(input)
    num_cols = len(input[0]) - 1

    seen = {}
    total_perimeter_cost = 0
    total_side_cost = 0
    for row_idx, row in enumerate(input):
        row = row.rstrip()
        for col_idx in range(num_rows):
            # Check if we've seen this node yet. If not, traverse its whole subgraph
            if (row_idx, col_idx) not in seen:
                (perimeter_cost, side_cost) = traverse_subgraph(input, row_idx, num_rows, col_idx, num_cols, seen)
                total_perimeter_cost += perimeter_cost
                total_side_cost += side_cost
    print(f"Perimeter Cost: {total_perimeter_cost}, Side cost: {total_side_cost}")

def traverse_subgraph(input, row_idx, num_rows, col_idx, num_cols, seen):
    to_visit = deque()
    to_visit.append((row_idx, col_idx))
    subgraph_area = 0
    subgraph_perimeter = 0
    subgraph_corners = 0

    # BFS to traverse the subgraph
    while len(to_visit) > 0:
        (row_idx, col_idx) = to_visit.popleft()
        # Check if we've already visited
        if (row_idx, col_idx) in seen:
            continue

        seen[(row_idx, col_idx)] = True
        this_plot_letter = input[row_idx][col_idx]
        subgraph_area += 1
        plot_neighbors = 0

        # check up for neighbor
        up = ''
        if row_idx > 0:
            up = input[row_idx - 1][col_idx] 
            if up == this_plot_letter:
                plot_neighbors += 1
                if (row_idx - 1, col_idx) not in seen:
                    to_visit.append((row_idx - 1, col_idx))
            else:
                up = ''

        # check down for neighbor
        down = ''
        if row_idx < num_rows - 1:
            down = input[row_idx + 1][col_idx] 
            if down == this_plot_letter:
                plot_neighbors += 1
                if (row_idx + 1, col_idx) not in seen:
                    to_visit.append((row_idx + 1, col_idx))
            else:
                down = ''
        
        # check left
        left = ''
        if col_idx > 0:
            left = input[row_idx][col_idx - 1] 
            if left == this_plot_letter:
                plot_neighbors += 1
                if (row_idx, col_idx - 1) not in seen:
                    to_visit.append((row_idx, col_idx - 1))
            else:
                left = ''

        # check right
        right = ''
        if col_idx < num_cols - 1:
            right = input[row_idx][col_idx + 1] 
            if right == this_plot_letter:
                plot_neighbors += 1
                if (row_idx, col_idx + 1) not in seen:
                    to_visit.append((row_idx, col_idx + 1))
            else:
                right = ''

        # look for "outside" corners
        #    _
        #   | |
        #
        if (not up and not left):
            subgraph_corners += 1
        if (not up and not right):
            subgraph_corners += 1
        if (not down and not left):
            subgraph_corners += 1
        if (not down and not right):
            subgraph_corners += 1

        # look for "inside" corners
        #     _
        #      |_
        #        |
        if (up and left) and not input[row_idx - 1][col_idx - 1] == this_plot_letter:
            subgraph_corners += 1
        if (up and right) and not input[row_idx - 1][col_idx + 1] == this_plot_letter:
            subgraph_corners += 1
        if (down and left) and not input[row_idx + 1][col_idx - 1] == this_plot_letter:
            subgraph_corners += 1
        if (down and right) and not input[row_idx + 1][col_idx + 1] == this_plot_letter:
            subgraph_corners += 1
        plot_edges = 4 - plot_neighbors
        subgraph_perimeter += plot_edges

    perimeter_cost = subgraph_area * subgraph_perimeter
    side_cost = subgraph_area * subgraph_corners
    return (perimeter_cost, side_cost)
            
main()