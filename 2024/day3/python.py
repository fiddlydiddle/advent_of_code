def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2024/day3/input.txt', 'r').readlines()
    
    total_string = ''
    for line in input:
        total_string += line

    part1_result = run_multiply_instructions(total_string)
    print(f"Part 1: {part1_result}") # Part 1

    # Part 2
    part2_result = 0
    current_start_idx = 0
    while True:
        # Find "don't()", process all the mul commands before it
        search_area = total_string[current_start_idx:]
        dont_idx = search_area.find("don't()")
        if dont_idx < 0:
            dont_idx = len(search_area) - 1
        to_parse = search_area[:dont_idx]
        part2_result += run_multiply_instructions(to_parse)

        # Look for next occurence of "do()"
        do_idx = search_area[dont_idx:].find("do()")
        if do_idx < 0:
            break
        else:
            current_start_idx += dont_idx + do_idx

    print(f"Part 2: {part2_result}")


def run_multiply_instructions(str):
    result = 0
    # find potential multiply instructions by splitting by 'mul'
    potential_muls = str.split('mul')
    for potential_mul in potential_muls:
        if not potential_mul:
            continue # nothing after 'mul'

        if not potential_mul[0] == '(': 
            continue # no opening parenthesis


        closing_paren_idx = potential_mul.find(')')
        if closing_paren_idx < 1:
            continue # no closing parenthesis
        else:
            if ' ' in potential_mul[:closing_paren_idx]:
                continue # leading or trailing space somewhere

            potential_operands = potential_mul[1:closing_paren_idx]

            nums = potential_operands.split(',')
            if len(nums) == 2:
                continue # don't have two comma-separated values
            else:
                try:
                    num1 = int(nums[0])
                    num2 = int(nums[1])
                    result += (num1 * num2)
                except:
                    continue # couldn't parse values to in and multiply

    return result


main()