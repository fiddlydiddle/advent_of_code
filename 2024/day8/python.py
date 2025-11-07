import math
import copy

def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2024/day8/example.txt', 'r').readlines()
    example_antipoles = part1(example_input)
    print(f"Part 1 example: {len(example_antipoles.keys())}")
    example_antipoles = part1(example_input, 200)
    print(f"Part 2 example: {len(example_antipoles.keys())}")

    input = open('/home/john/Documents/Projects/advent_of_code/2024/day8/input.txt', 'r').readlines()
    part1_antipoles = part1(input)
    print(f"Part 1: {len(part1_antipoles.keys())}")
    part2_antipoles = part1(input, 200)
    print(f"Part 2: {len(part2_antipoles.keys())}")
    

def part1(input, num_repititions = 0):
    height = len(input)
    width = len(input[0]) - 1
    antennas = {}

    # Find all the antennas in the input and note their locations
    for row_idx, line in enumerate(input):
        line = line.strip()
        for col_idx, char in enumerate(line):
            if char != '.':
                if char in antennas:
                    antennas[char].append((row_idx, col_idx))
                else:
                    antennas[char] = [(row_idx, col_idx)]

    # Run through antennas and note all antipole positions
    antipoles = {}
    for frequency in antennas.keys():
        for idx, antenna1 in enumerate(antennas[frequency]):
            antenna1_row, antenna1_col = antenna1
            for antenna2 in antennas[frequency][idx+1:]:
                antenna2_row, antenna2_col = antenna2
                # Find row and col differences between two antennas
                row_diff = antenna2_row - antenna1_row
                col_diff = antenna2_col - antenna1_col

                # Two antennas will create two antipoles, one on each side
                frequency_antipoles = []
                iteration_range = [1] if not num_repititions else range(num_repititions)
                for i in iteration_range:
                    frequency_antipoles.append((antenna1_row - (i * row_diff), antenna1_col - (i * col_diff)))
                    frequency_antipoles.append((antenna2_row + (i * row_diff), antenna2_col + (i * col_diff)))

                # Check if antipoles are in bounds
                for frequeny_antipole in frequency_antipoles:
                    if is_inbounds(frequeny_antipole[0], frequeny_antipole[1], width, height):
                        antipole_str = f"{frequeny_antipole[0]},{frequeny_antipole[1]}"
                        if antipole_str in antipoles:
                            antipoles[antipole_str].add(frequency)
                        else:
                            antipoles[antipole_str] = set(frequency)  

    return antipoles


def is_inbounds(row, col, width, height):
    return row >= 0 and row < height and col >= 0 and col < width

main()