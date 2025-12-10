import copy

def part1(stone_list, num_blinks):
    stone_list_copy = copy.deepcopy(stone_list)
    for _ in range(num_blinks):
        for idx in range(len(stone_list_copy)):
            stone_val = stone_list_copy[idx]
            if stone_val == '0':
                stone_list_copy[idx] = '1'
            elif len(stone_val) % 2 == 0:
                first_half = stone_val[:len(stone_val) // 2]
                second_half = stone_val[len(stone_val) // 2:]
                stone_list_copy[idx] = first_half
                stone_list_copy.append(str(int(second_half)))
            else:
                stone_list_copy[idx] = str(int(stone_val) * 2024)

    return len(stone_list_copy)

def part2(stone_list, num_blinks):
    # memo will store (stone_val, depth) tuples and their results
    # depth is important since if we see e.g. '1' at depth 1 the result is
    # different than if we see '1' at depth 23
    memo = {}

    def dfs(stone_val, depth):
        # check if we've hit a leaf
        if depth == num_blinks + 1:
            return 1
        
        # Check if we've seen this value before
        if (depth, stone_val) in memo:
            return memo[(depth, stone_val)]
        
        # drill baby drill
        result = 0
        if stone_val == '0':
            result += dfs('1', depth + 1)
        elif len(stone_val) % 2 == 0:
            first_half = stone_val[:len(stone_val) // 2]
            second_half = stone_val[len(stone_val) // 2:]
            result += dfs(first_half, depth + 1)
            result += dfs(str(int(second_half)), depth + 1)
        else:
            result += dfs(str(int(stone_val) * 2024), depth + 1)

        # memoize and return
        memo[(depth, stone_val)] = result
        return result

    result = 0
    depth = 0
    for stone in stone_list:
        result += dfs(stone, depth + 1)

    return result

def main():
    example_input = open('./example.txt', 'r').read().split()
    input = open('./input.txt', 'r').read().split()

    # Part 1 Example (55312)
    part1_example_result = part2(example_input, 6)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1 (233875)
    part1_result = part2(input, 25)
    print(f"Part 1: {part1_result}")

    # Part 2 (277444936413293)
    part2_result = part2(input, 75)
    print(f"Part 2: {part2_result}")

main()