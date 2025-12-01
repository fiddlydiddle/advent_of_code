import math

def part1(input):
    current_val = 50
    result = 0

    for line in input:
        # Parse line for direction and steps
        direction = line[0]
        sign = 1 if direction == 'R' else -1
        steps = int(line[1:])

        # Perform steps in direction
        current_val += (steps * sign)

        # Take modulus to handle dial wrapping
        current_val %= 100

        # Increment result if we land on 0
        if current_val == 0:
            result += 1

    return result

def part2(input):
    current_val = 50
    result = 0

    for line in input:
        # Parse line for direction and steps
        direction = line[0]
        sign = 1 if direction == 'R' else -1
        steps = int(line[1:])

        for _ in range(steps):
            # Perform a step in direction
            current_val += sign

            # Take modulus to handle dial wrapping
            current_val %= 100

            # Increment result if we land on 0
            if current_val == 0:
                result += 1

    return result

def part2_2(input):
    current_val = 50
    result = 0

    for line in input:
        direction = line[0]
        sign = 1 if direction == 'R' else -1
        steps = int(line[1:])
        
        change = steps * sign
        
        old_position = current_val
        new_position = old_position + change
        
        if change > 0:
            # Take floor of new_position divided by 100. Same for old_position.
            # Num zeroes is the difference between the two.
            old_loops = old_position // 100
            new_loops = new_position // 100
            result += (new_loops - old_loops)
        elif change <= 0:
            # Take ceiling of new_position divided by 100. Same for old_position
            # Num zeros is the defference between the two.
            old_loops = math.ceil(old_position / 100.0) - 1
            new_loops = math.ceil(new_position / 100.0) - 1
            result += (old_loops - new_loops)

        current_val = new_position % 100
        
    return result


def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2025/day1/example.txt', 'r').read().strip().split('\n')
    input = open('/home/john/Documents/Projects/advent_of_code/2025/day1/input.txt', 'r').read().strip().split('\n')

    # # Part 1 Example
    result = part1(example_input)
    print(f"Part 1 (example): {result}")

    # Part 1
    result = part1(input)
    print(f"Part 1: {result}")

    # Part 2 Example
    result = part2(example_input)
    print(f"Part 2 (example): {result}")

    # Part 2
    result = part2(input)
    print(f"Part 2: {result}")

    # Part 2 Optimized
    result = part2_2(input)
    print(f"Part 2 (Optimized): {result}")

main()