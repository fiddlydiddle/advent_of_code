# Now deprecated, part2 does both parts of the problem
def part1(input):
    first_beam_col = input[0].index('S')
    beam_cols = set([first_beam_col])

    part1_result = 0
    # Move from top to bottom one step at a time and simulate the beams' path
    for row_idx in range(len(input)):
        beams_to_remove = []
        beams_to_add = []

        # For each existing beam, check if it hits a splitter
        for col_idx in beam_cols:
            if input[row_idx][col_idx] == '^':
                # Hit a splitter. Increment counter and split beam
                part1_result += 1
                # Take note of beams to add and remove (can't mutate beam_cols while iterating through it)
                beams_to_remove.append(col_idx)
                beams_to_add.append(col_idx - 1)
                beams_to_add.append(col_idx + 1)

        # Add and remove beams
        beam_cols -= set(beams_to_remove)
        beam_cols.update(beams_to_add)

    return part1_result

def part2(input):
    first_beam_col = input[0].index('S')
    beam_cols = { first_beam_col: 1 } # Map to keep track of how many beams occupy a given column

    # Move from top to bottom one step at a time and simulate the beams' path
    part1_result = 0
    for row_idx in range(len(input)):
        beams_to_add = []
        beams_to_remove = []

        # For each beam column, check if we hit a splitter
        for col_idx in beam_cols.keys():
            if input[row_idx][col_idx] == '^':
                part1_result += 1
                # When hitting a splitter, all beams on current col move left one col and right one col
                # Take note of what to add (can't mutate keys of the map while iterating over them)
                num_beams = beam_cols[col_idx]
                beams_to_add.extend([(col_idx - 1, num_beams), (col_idx + 1, num_beams)])
                beams_to_remove.append(col_idx)

        # Add/update the new beam columns
        for beam_col in beams_to_remove:
            del beam_cols[beam_col]
        for beam_col, num_beams in beams_to_add:
            beam_cols[beam_col] = beam_cols.get(beam_col, 0) + num_beams

    return part1_result, sum(beam_cols.values())

def part2_recursive(input: list[str]):
    # DFS with memoization
    def dfs(row_idx, col_idx, memo):
        # Check if we've already been here
        if (row_idx, col_idx) in memo:
            return memo[(row_idx, col_idx)]
        
        # Check if we hit bottom
        if row_idx == len(input):
            return 1
        
        # Drill baby, drill
        result = None
        if input[row_idx][col_idx] == '^':
            left = dfs(row_idx + 1, col_idx - 1, memo)
            right = dfs(row_idx + 1, col_idx + 1, memo)
            result = left + right
        else:
            result = dfs(row_idx + 1, col_idx, memo)

        # Memoize result
        memo[(row_idx, col_idx)] = result
        return result
        
    first_beam_col = input[0].index('S')
    memo = { (0, first_beam_col): 1 }
    return dfs(1, first_beam_col, memo)


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 & 2 Example
    part1_example_result, part2_example_result = part2(example_input)
    print(f"Part 1 (example): {part1_example_result}")
    print(f"Part 2 (example): {part2_example_result}")

    # Part 1 & 2
    part1_result, part2_result = part2(input)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

    # Part 2 (Recursive)
    part2_recursive_result = part2_recursive(input)
    print(f"Part 2 (Recursive): {part2_recursive_result}")

main()