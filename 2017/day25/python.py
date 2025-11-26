def part1():
    tape_size = 15_000 # Hard-coded after trial and error
    tape = bytearray(tape_size)
    current_state = 'a'
    current_idx = tape_size // 2
    checksum_steps = 12_386_363
    checksum_count = 0

    for _ in range(checksum_steps):
        current_val = tape[current_idx]
        if current_state == 'a':
            if current_val == 0:
                tape[current_idx] = 1
                checksum_count += 1
                current_idx += 1
                current_state = 'b'
            else:
                tape[current_idx] = 0
                checksum_count -= 1
                current_idx -= 1
                current_state = 'e'
        elif current_state == 'b':
            if current_val == 0:
                tape[current_idx] = 1
                checksum_count += 1
                current_idx -= 1
                current_state = 'c'
            else:
                tape[current_idx] = 0
                checksum_count -= 1
                current_idx += 1
                current_state = 'a'
        elif current_state == 'c':
            if current_val == 0:
                tape[current_idx] = 1
                checksum_count += 1
                current_idx -= 1
                current_state = 'd'
            else:
                tape[current_idx] = 0
                checksum_count -= 1
                current_idx += 1
                current_state = 'c'
        elif current_state == 'd':
            if current_val == 0:
                tape[current_idx] = 1
                checksum_count += 1
                current_idx -= 1
                current_state = 'e'
            else:
                tape[current_idx] = 0
                checksum_count -= 1
                current_idx -= 1
                current_state = 'f'
        elif current_state == 'e':
            if current_val == 0:
                tape[current_idx] = 1
                checksum_count += 1
                current_idx -= 1
                current_state = 'a'
            else:
                current_idx -= 1
                current_state = 'c'
        elif current_state == 'f':
            if current_val == 0:
                tape[current_idx] = 1
                checksum_count += 1
                current_idx -= 1
                current_state = 'e'
            else:
                current_idx += 1
                current_state = 'a'

    return checksum_count

def main():
    # Part 1
    # input = open('/home/john/Documents/Projects/advent_of_code/2017/day25/input.txt', 'r').readlines()
    result = part1()
    print(f"Part 1: {result}")

main()