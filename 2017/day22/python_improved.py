def part2(num_bursts):
    input = open('/home/john/Documents/Projects/advent_of_code/2017/day22/input.txt', 'r').readlines()

    path_map = {}
    for row_idx, line in enumerate(input):
        line = line.rstrip()
        for col_idx, char in enumerate(line):
            if char != '.':
                path_map[(row_idx, col_idx)] = char

    result = 0
    height = len(input)
    width = len(input[0]) - 1 # Input lines end with new-line character
    current_row = height // 2
    current_col = width // 2
    current_direction = "up"

    right_turn_map = {
        "right": "down",
        "down": "left",
        "left": "up",
        "up": "right"
    }

    left_turn_map = {
        "left": "down",
        "down": "right",
        "right": "up",
        "up": "left"
    }

    for _ in range(num_bursts):
        position_key = (current_row, current_col)

        # Assume current position is clean unless we find otherwise in the path map
        current_val = path_map.get(position_key, '.')

        # Look at current node. Turn based on node's infected status. Flip the infected status
        if current_val == '#':
            # Currently infected
            current_direction = right_turn_map[current_direction]
            path_map[position_key] = '!'
        elif current_val == '.':
            # Currently clean
            current_direction = left_turn_map[current_direction]
            path_map[position_key] = '@'
        elif current_val == '@':
            # Currently weakened
            path_map[position_key] = '#'
            result += 1
        elif current_val == '!':
            # Currently flagged
            current_direction = right_turn_map[right_turn_map[current_direction]] # turn right twice to reverse
            del path_map[position_key]

        # Take one step in current direction
        if current_direction == 'up':
            current_row -= 1
        elif current_direction == 'down':
            current_row += 1
        elif current_direction == 'right':
            current_col += 1
        else:
            current_col -= 1

    print(f"Part 2: {result}")

part2(10_000_000)