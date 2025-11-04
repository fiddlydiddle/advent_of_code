# Just played whack-a-mole with this one to get string slicing and dicing to work
def main():
    starting_shape = ['.#.','..#','###']

    example_input = open('/home/john/Documents/Projects/advent_of_code/2017/day21/example.txt', 'r').readlines()
    example_pattern_rules = parse_input_rules(example_input)
    part1_example_result = part1(starting_shape, example_pattern_rules, 2)
    print(f"Part 1 (example): {to_pattern_string(part1_example_result).count('#')}")

    part1_input = open('/home/john/Documents/Projects/advent_of_code/2017/day21/input.txt', 'r').readlines()
    part1_pattern_rules = parse_input_rules(part1_input)
    part1_result = part1(starting_shape, part1_pattern_rules, 5)
    print(f"Part 1: {to_pattern_string(part1_result).count('#')}")

    part2_result = part1(starting_shape, part1_pattern_rules, 18)
    print(f"Part 2: {to_pattern_string(part2_result).count('#')}")

def part1(starting_shape, pattern_rules, num_iterations):
    result_shape = starting_shape
    for i in range(num_iterations):
        size = len(result_shape)

        # Split even-number size grid into many 2x2 grids
        if size % 2 == 0:
            items_per_row = size // 2
            num_pieces = items_per_row ** 2
            new_shape = [''] * (items_per_row * 3)
            for j in range(num_pieces):
                # Find piece in current shape
                start_row = 2 * (j // items_per_row)
                start_col = (2 * j) % size
                piece = [
                    result_shape[start_row][start_col:start_col+2],
                    result_shape[start_row + 1][start_col:start_col+2]
                ]

                # Flip and rotate piece until it matches a rule
                new_piece = apply_rule(piece, pattern_rules)

                # Apply rule and update new shape
                new_piece = to_pattern_array(new_piece)
                new_shape[(3 * (j // items_per_row)) + 0] += new_piece[0]
                new_shape[(3 * (j // items_per_row)) + 1] += new_piece[1]
                new_shape[(3 * (j // items_per_row)) + 2] += new_piece[2]

            result_shape = new_shape
        # split non-even-number size grid into 3x3 grids
        else:
            items_per_row = size // 3
            num_pieces = items_per_row ** 2
            new_shape = [''] * (items_per_row * 4)
            for j in range(num_pieces):
                # Find piece in current shape
                start_row = 3 * (j // items_per_row)
                start_col = (3 * j) % size
                piece = [
                    result_shape[start_row][start_col:start_col+3],
                    result_shape[start_row + 1][start_col:start_col+3],
                    result_shape[start_row + 2][start_col:start_col+3]
                ]

                # Flip and rotate piece until it matches a rule
                new_piece = apply_rule(piece, pattern_rules)

                # Apply rule and update new shape
                new_piece = to_pattern_array(new_piece)
                new_shape[(4 * (j // items_per_row)) + 0] += new_piece[0]
                new_shape[(4 * (j // items_per_row)) + 1] += new_piece[1]
                new_shape[(4 * (j // items_per_row)) + 2] += new_piece[2]
                new_shape[(4 * (j // items_per_row)) + 3] += new_piece[3]

            result_shape = new_shape

    return result_shape

def apply_rule(piece, pattern_rules):
    new_piece = None
    num_rotations = 0
    while not new_piece and num_rotations < 4:
        if to_pattern_string(piece) in pattern_rules:
            new_piece = pattern_rules[to_pattern_string(piece)]
        else:
            piece = rotate_piece(piece)
            if to_pattern_string(piece) in pattern_rules:
                new_piece = pattern_rules[to_pattern_string(piece)]
            else:
                flipped_piece = flip_piece(piece)
                if to_pattern_string(flipped_piece) in pattern_rules:
                    new_piece = pattern_rules[to_pattern_string(flipped_piece)]

        num_rotations += 1

    return new_piece

def rotate_piece(piece):
    return [''.join(column) for column in zip(*piece)][::-1]
    
def flip_piece(piece):
    return [row[::-1] for row in piece]

def to_pattern_string(piece):
    return "/".join(piece)

def to_pattern_array(piece):
    return piece.split('/')

def parse_input_rules(input):
    pattern_rules = {}
    for line in input:
        line = line.rstrip()
        input_pattern, output_pattern = line.split(' => ')
        pattern_rules[input_pattern] = output_pattern
    return pattern_rules

main()