def part1(ranges, ingredients):
    result = 0

    # Check if each ingredient falls into a range
    for ingredient in ingredients:
        matching_ranges = list(filter(lambda range: range[0] <= ingredient <= range[1], ranges))
        if len(matching_ranges) > 0:
            result += 1

    return result

def part2(unmerged_ranges):
    sorted_ranges = sorted(unmerged_ranges, key=lambda range: range[0])
    result = 0

    low_val = sorted_ranges[0][0]
    high_val = sorted_ranges[0][1]

    for idx in range(1, len(sorted_ranges)):
        current_range = sorted_ranges[idx]
        last_range = sorted_ranges[idx - 1]
        
        if current_range[0] <= last_range[1]:
            # Current range overlaps with previous
            # Keep low_val and set high_val to max
            high_val = max(current_range[1], last_range[1])
        else:
            # No overlap with previous range
            # Add previous range to result and start new low_val, high_val
            result += high_val - low_val + 1
            low_val = current_range[0]
            high_val = current_range[1]

    result += high_val - low_val + 1
    return result


def parse_input(input):
    ranges = []
    ingredients = []
    parsing_ranges = True

    # First pass, extract ranges and ingredients
    for line in input:
        # Hit division between ranges and ingredients
        if line == '':
            parsing_ranges = False
            continue

        if parsing_ranges:
            low_val, high_val = line.split('-')
            ranges.append((int(low_val), int(high_val)))
        else:
            ingredients.append(int(line))
        
    return ranges, ingredients

def main():
    example_input = open('./example.txt', 'r').read().strip().split('\n')
    example_ranges, example_ingredients = parse_input(example_input)
    input = open('./input.txt', 'r').read().strip().split('\n')
    ranges, ingredients = parse_input(input)

    # Part 1 Example
    result = part1(example_ranges, example_ingredients)
    print(f"Part 1 (example): {result}")

    # Part 1
    result = part1(ranges, ingredients)
    print(f"Part 1: {result}")

    # Part 2 Example
    result = part2(example_ranges)
    print(f"Part 2 (example): {result}")

    # Part 2
    result = part2(ranges)
    print(f"Part 2: {result}")

main()