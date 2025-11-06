import math
import copy

def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2024/day6/example.txt', 'r').readlines()
    example_guard_path = part1(example_input)
    print(f"Part 1 example: {len(example_guard_path.keys())}")
    part2_example_result = part2(example_input, example_guard_path)
    print(f"Part 2 example: {part2_example_result}")

    part1_input = open('/home/john/Documents/Projects/advent_of_code/2024/day6/input.txt', 'r').readlines()
    part1_guard_path = part1(part1_input)
    print(f"Part 1: {len(part1_guard_path.keys())}")
    part2_result = part2(part1_input, part1_guard_path)
    print(f"Part 2: {part2_result}")

def part2(input, guard_path):
    path_squares = guard_path.keys()
    result = 0
    for square in path_squares:
        row, col = square.split(',')
        row = int(row)
        col = int(col)
        input_copy = copy.deepcopy(input)
        input_copy = place_obstacle(input_copy, row, col)
        if part1(input_copy, 10_000) == "infinite":
            result += 1

    return result

def part1(input, max_steps=math.inf):
    height = len(input)
    width = len(input[0]) - 1 # Input contains new line characters
    current_row = 0
    current_col = 0
    current_direction = 'up'
    guard_path = {}
    num_steps = 0

    # Find initial position of guard
    for idx, line in enumerate(input):
        if line.find('^') > -1:
            current_row = idx
            current_col = line.find('^')
            break

    # Walk the guard's path
    while is_inbounds(current_row, current_col, width, height) and num_steps < max_steps:
        next_row = current_row
        next_col = current_col

        # Figure out guard's next position
        if current_direction == 'up':
            next_row -= 1
        elif current_direction == 'right':
            next_col += 1
        elif current_direction == 'down':
            next_row += 1
        else:
            next_col -= 1

        # Check boundary condition
        if not is_inbounds(next_row, next_col, width, height):
            return guard_path # Guard has left the area

        # Check for obstacle. It's possible to turn and immediately hit another obstacle
        while input[next_row][next_col] == '#':
            if current_direction == 'up':
                current_direction = 'right'
                next_row = current_row
                next_col = current_col + 1
            elif current_direction == 'right':
                current_direction = 'down'
                next_row = current_row + 1
                next_col = current_col
            elif current_direction == 'down':
                current_direction = 'left'
                next_row = current_row
                next_col = current_col - 1
            else:
                current_direction = 'up'
                next_row = current_row - 1
                next_col = current_col

        # Take step
        current_row = next_row
        current_col = next_col
        num_steps += 1

        # Record path taken
        if f"{current_row},{current_col}" in guard_path:
            guard_path[f"{current_row},{current_col}"] += 1
        else:
            guard_path[f"{current_row},{current_col}"] = 1

    if num_steps == max_steps:
        return "infinite"

    return guard_path # Guard has left the area

def is_inbounds(row, col, width, height):
    return row >= 0 and row < height and col >= 0 and col < width

def place_obstacle(input, row, col):
    row_string = input[row]
    row_string = row_string[:col] + '#' + row_string[col+1:]
    input[row] = row_string
    return input

main()