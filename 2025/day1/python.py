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

main()