import copy

NEIGHBOR_OFFSETS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

def part1(input, remove_rolls = False):
    new_input = copy.deepcopy(input)
    height = len(new_input)
    width = len(new_input[0])
    rolls_removed = 0

    # Run through grid and stop at '@' spots. Check for neighbors
    for row_idx, row in enumerate(new_input):
        for col_idx, col in enumerate(row):
            if col == '@':
                num_neighbors = 0

                # Check for neighboring '@'
                for i in range(9):
                    neighbor_row_idx = row_idx + (i // 3) - 1
                    neighbor_col_idx = col_idx + (i % 3) - 1

                    # Boundary check
                    if is_inbounds(neighbor_row_idx, neighbor_col_idx, width, height):
                        # Exclude own position from check, otherwise check for '@'
                        if input[neighbor_row_idx][neighbor_col_idx] == '@' and not (neighbor_row_idx == row_idx and neighbor_col_idx == col_idx):
                            num_neighbors += 1

                # Roll can be removed
                if num_neighbors < 4:
                    rolls_removed += 1
                    if remove_rolls:
                        new_input[row_idx][col_idx] = '.'

    return new_input, rolls_removed

def part1_optimized(input, remove_rolls = False):
    new_input = [row[:] for row in input]
    height = len(new_input)
    width = len(new_input[0])
    rolls_removed = 0

    # Run through grid and stop at '@' spots. Check for neighbors
    for row_idx, row in enumerate(new_input):
        for col_idx, col in enumerate(row):
            if col == '@':
                num_neighbors = 0

                # Check for neighboring '@'
                for row_offset, col_offset in NEIGHBOR_OFFSETS:
                    neighbor_row_idx = row_idx + row_offset
                    neighbor_col_idx = col_idx + col_offset

                    # Boundary check
                    if is_inbounds(neighbor_row_idx, neighbor_col_idx, width, height):
                        # Exclude own position from check, otherwise check for '@'
                        if new_input[neighbor_row_idx][neighbor_col_idx] == '@':
                            num_neighbors += 1

                # Roll can be removed
                if num_neighbors < 4:
                    rolls_removed += 1
                    if remove_rolls:
                        new_input[row_idx][col_idx] = '.'

    return new_input, rolls_removed


def part2(input):
    new_input = [row[:] for row in input]
    result = 0

    num_rolls_removed = 1

    # Wrap Part 1 in loop that terminates once a round does not remove any rolls
    while num_rolls_removed > 0:
        new_input, num_rolls_removed = part1_optimized(new_input, True)
        result += num_rolls_removed

    return result
    

def is_inbounds(row, col, width, height):
    return row >= 0 and row < height and col >= 0 and col < width


def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2025/day4/example.txt', 'r').read().strip().split('\n')
    example_input = [list(row) for row in example_input]
    input = open('/home/john/Documents/Projects/advent_of_code/2025/day4/input.txt', 'r').read().strip().split('\n')
    input = [list(row) for row in input]

    # Part 1 Example
    _, result = part1(example_input)
    print(f"Part 1 (example): {result}")

    # Part 1
    _, result = part1(input)
    print(f"Part 1: {result}")

    # Part 2 Example
    result = part2(example_input)
    print(f"Part 2 (example): {result}")

    # Part 2
    result = part2(input)
    print(f"Part 2: {result}")

main()