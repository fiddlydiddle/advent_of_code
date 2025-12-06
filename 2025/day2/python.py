def part1(input):
    result = 0
    for line in input:
        start_val, end_val = line.split('-')
        start_val = int(start_val)
        end_val = int(end_val)

        for val_to_check in range(start_val, end_val + 1):
            val_length = len(str(val_to_check))
            # Take substrings of size j // 2 and see if they are repeated 
            if val_length % 2 == 0:
                substring = str(val_to_check)[:val_length//2]
                if substring * 2 == str(val_to_check):
                    result += val_to_check

    return result

def part2(input):
    result = 0
    for line in input:
        start_val, end_val = line.split('-')
        start_val = int(start_val)
        end_val = int(end_val)

        for val_to_check in range(start_val, end_val + 1):
            val_length = len(str(val_to_check))
            # Take substrings of size i and see if they are repeated 
            for i in range(1, val_length // 2 + 1):
                if val_length % i == 0:
                    substring = str(val_to_check)[:i]
                    num_repititions = val_length // i
                    if substring * num_repititions == str(val_to_check):
                        result += val_to_check
                        break

    return result

def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2025/day2/example.txt', 'r').read().strip().split(',')
    input = open('/home/john/Documents/Projects/advent_of_code/2025/day2/input.txt', 'r').read().strip().split(',')

    # # Part 1 Example
    # result = part1(example_input)
    # print(f"Part 1 (example): {result}")

    # # Part 1
    # result = part1(input)
    # print(f"Part 1: {result}")

    # # Part 2 Example
    # result = part2(example_input)
    # print(f"Part 2 (example): {result}")

    # Part 2
    result = part2(input)
    print(f"Part 2: {result}")

main()