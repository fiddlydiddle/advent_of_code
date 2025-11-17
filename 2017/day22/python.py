def part1(input, num_bursts):
    result = 0
    height = len(input)
    width = len(input[0]) - 1 # Input lines end with new-line character
    current_row = height // 2
    current_col = width // 2
    current_direction = "up"

    for _ in range(num_bursts):
        current_val = input[current_row][current_col]

        # Look at current node. Turn based on node's infected status. Flip the infected status
        if current_val == '#':
            current_direction = turn_right(current_direction)
            input[current_row] = input[current_row][:current_col] + '.' + input[current_row][current_col + 1:]
        else:
            current_direction = turn_left(current_direction)
            input[current_row] = input[current_row][:current_col] + '#' + input[current_row][current_col + 1:]
            result += 1

        # Take one step in current direction
        current_row, current_col = take_step(current_row, current_col, current_direction)

        # Check if we've left the area
        if not is_inbounds(current_row, current_col, width, height):
            input = expand_input(input)
            current_row += 1
            current_col += 1
            height += 2
            width += 2

    return result

def part2(input, num_bursts):
    result = 0
    height = len(input)
    width = len(input[0]) - 1 # Input lines end with new-line character
    current_row = height // 2
    current_col = width // 2
    current_direction = "up"

    for _ in range(num_bursts):
        current_val = input[current_row][current_col]

        # Look at current node. Turn based on node's infected status. Flip the infected status
        if current_val == '#':
            # Currently infected
            current_direction = turn_right(current_direction)
            input[current_row] = input[current_row][:current_col] + '!' + input[current_row][current_col + 1:]
        elif current_val == '.':
            # Currently clean
            current_direction = turn_left(current_direction)
            input[current_row] = input[current_row][:current_col] + '@' + input[current_row][current_col + 1:]
        elif current_val == '@':
            # Currently weakened
            input[current_row] = input[current_row][:current_col] + '#' + input[current_row][current_col + 1:]
            result += 1
        elif current_val == '!':
            # Currently flagged
            current_direction = turn_right(turn_right(current_direction)) # turn right twice to reverse
            input[current_row] = input[current_row][:current_col] + '.' + input[current_row][current_col + 1:]

        # Take one step in current direction
        current_row, current_col = take_step(current_row, current_col, current_direction)

        # Check if we've left the area
        if not is_inbounds(current_row, current_col, width, height):
            input = expand_input(input)
            current_row += 1
            current_col += 1
            height += 2
            width += 2

    return result

def take_step(current_row, current_col, current_direction):
    if current_direction == 'up':
        current_row -= 1
    elif current_direction == 'down':
        current_row += 1
    elif current_direction == 'right':
        current_col += 1
    else:
        current_col -= 1

    return current_row, current_col

def turn_right(current_direction):
    turn_map = {
        "right": "down",
        "down": "left",
        "left": "up",
        "up": "right"
    }
    return turn_map[current_direction]

def turn_left(current_direction):
    turn_map = {
        "left": "down",
        "down": "right",
        "right": "up",
        "up": "left"
    }
    return turn_map[current_direction]

def is_inbounds(row, col, width, height):
    return row >= 0 and row < height and col >= 0 and col < width

def expand_input(input):
    width = len(input[0])
    if '\n' in input[0]:
        width -= 1

    new_input = []
    new_input.append('.' * (width + 2))
    for line in input:
        line = line.rstrip()
        new_line = '.' + line + '.'
        new_input.append(new_line)
    new_input.append('.' * (width + 2))

    return new_input

def main():
    # # Part 1 short example
    # example_input = open('/home/john/Documents/Projects/advent_of_code/2017/day22/example.txt', 'r').readlines()
    # example_result = part1(example_input, 70)
    # print(f"Part 1 example (70 bursts): {example_result}")

    # # Part 1 full example
    # example_input = open('/home/john/Documents/Projects/advent_of_code/2017/day22/example.txt', 'r').readlines()
    # example_result = part1(example_input, 10_000)
    # print(f"Part 1 example (10,000 bursts): {example_result}")

    # # Part 1
    # input = open('/home/john/Documents/Projects/advent_of_code/2017/day22/input.txt', 'r').readlines()
    # result = part1(input, 10_000)
    # print(f"Part 1: {result}")

    # # Part 2 short example
    # example_input = open('/home/john/Documents/Projects/advent_of_code/2017/day22/example.txt', 'r').readlines()
    # example_result = part2(example_input, 100)
    # print(f"Part 2 example (100 bursts): {example_result}")

    # # Part 2 full example
    # example_input = open('/home/john/Documents/Projects/advent_of_code/2017/day22/example.txt', 'r').readlines()
    # example_result = part2(example_input, 10_000_000)
    # print(f"Part 2 example (10,000,000 bursts): {example_result}")

    # Part 2
    input = open('/home/john/Documents/Projects/advent_of_code/2017/day22/input.txt', 'r').readlines()
    result = part2(input, 10_000_000)
    print(f"Part 2: {result}")

main()