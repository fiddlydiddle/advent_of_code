from collections import defaultdict
from functools import cmp_to_key

def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2024/day5/example.txt', 'r').readlines()
    example_result_part1, example_result_part2 = part1(example_input)
    print(f"Part 1 example: {example_result_part1}")
    print(f"Part 2 example: {example_result_part2}")

    part1_input = open('/home/john/Documents/Projects/advent_of_code/2024/day5/input.txt', 'r').readlines()
    part1_result, part2_result = part1(part1_input)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

def part1(input):
    # Rules will be a map of page number keys and values that are a list of pages that must come before they key
    rules = defaultdict(set)
    part1_result = 0
    part2_result = 0
    for line in input:
        # Check for blank line
        line = line.rstrip()
        if not line:
            continue

        # "Rule" lines have a pipe "|"
        if line.find('|') > -1:
            first, second = line.split('|')
            rules[first].add(second)
        else:
            # Updates are any lines without a pipe. Check if update is valid
            seen_pages = {}
            update = line.split(',')
            is_valid = True
            
            # Go page by page in update and check if we've already seen any
            # pages that are supposed to come after the current page
            for idx, page in enumerate(update):
                if page in rules:
                    after_pages = rules[page]
                    for after_page in after_pages:
                        if after_page in seen_pages:
                            is_valid = False
                if page not in seen_pages:
                    seen_pages[page] = idx

            if is_valid:
                part1_result += int(update[len(update) // 2])
            else:
                # Sort the incorrectly ordered update using custom comparator
                def compare_pages(a, b):
                    if b in rules[a]:
                        return -1
                    if a in rules[b]:
                        return 1
                    return 0
                sort_key = cmp_to_key(compare_pages)
                sorted_update = sorted(update, key=sort_key)
                part2_result += int(sorted_update[len(sorted_update) // 2])

    return part1_result, part2_result

main()