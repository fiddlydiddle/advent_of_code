def part1(input):
    result = 0
    for battery_bank in input:
        # Keep track of the great significant and insignificant digits seen so far
        max_significant_digit = 0
        max_insignificant_digit = 0
        for idx in range(len(battery_bank)):
            digit = int(battery_bank[idx])
            # Check if this digit is greatest significant digit
            # The last digit of the bank cannot be the greatest significant digit
            if idx < len(battery_bank) - 1 and digit > max_significant_digit:
                max_significant_digit = digit
                # Reset insignificant digit every time we find a new greatest significant digit
                max_insignificant_digit = 0
            elif digit > max_insignificant_digit:
                # If current digit is not greatest significant digit, check if it's the greatest insignificant digit
                max_insignificant_digit = digit

        bank_value = (max_significant_digit * 10) + max_insignificant_digit
        result += bank_value

    return result

def part2(input):
    result = 0
    for battery_bank in input:
        bank_value = 0
        digits_remaining = 12
        significant_digit_index = 0

        # Build bank_value one digit at a time
        # Use a sliding window to specify a search window for the next digit
        while digits_remaining > 0:
            max_significant_digit = 0

            # Sliding window starts on the index after the last digit we found
            # It ends at (length of banks) - (digits remaining)
            # e.g if bank is 987654321 and we still need 6 digits, the search area is 9876
            for idx in range(significant_digit_index, len(battery_bank) - digits_remaining + 1):
                digit = int(battery_bank[idx])
                if digit > max_significant_digit:
                    max_significant_digit = digit
                    significant_digit_index = idx + 1
            bank_value += max_significant_digit * (10 ** (digits_remaining - 1))
            digits_remaining -= 1

        result += bank_value

    return result


def main():
    example_input = open('/home/john/Documents/Projects/advent_of_code/2025/day3/example.txt', 'r').read().strip().split('\n')
    input = open('/home/john/Documents/Projects/advent_of_code/2025/day3/input.txt', 'r').read().strip().split('\n')

    # Part 1 Example
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