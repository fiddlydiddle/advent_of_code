import math
import copy

def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2024/day7/example.txt', 'r').readlines()
    example_result = part1(example_input)
    print(f"Part 1 example: {example_result}")

    part1_input = open('/home/john/Documents/Projects/advent_of_code/2024/day7/input.txt', 'r').readlines()
    part1_result = part1(part1_input)
    print(f"Part 1 example: {part1_result}")
    

def part1(input):
    result = 0

    # Go through each line in input and check if operations
    # can be applied to operands to get target value
    for line in input:
        line = line.strip()
        target_value, operands = line.split(':')
        target_value = int(target_value)
        operands = operands.strip().split(' ')
        # BFS: apply + an * to existing running totals to get all combinations of operations on operands
        running_totals = [0]
        for idx, operand in enumerate(operands):
            operand = int(operand)
            found_target = False
            new_totals = []
            for running_total in running_totals:
                new_addition = operand + running_total
                new_multiplication = operand * running_total
                new_concatenation = int(str(running_total) + str(operand)) # Part 2
                if (new_addition == target_value or new_multiplication == target_value or new_concatenation == target_value) and idx == len(operands) - 1:
                    result += target_value
                    found_target = True
                    break
                
                if new_addition <= target_value:
                    new_totals.append(new_addition)
                if new_multiplication <= target_value:
                    new_totals.append(new_multiplication)
                # Part 2
                if new_concatenation <= target_value:
                    new_totals.append(new_concatenation)

            running_totals = new_totals
            if found_target:
                break

    return result

main()