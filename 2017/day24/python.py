def part1(input):
    part1_best_strength = 0
    part2_best_strength = 0
    part2_best_length = 0

    # Try all combos and keep running tally of best strength
    def dfs(port_size, current_strength, visited_indices):
        nonlocal part1_best_strength
        nonlocal part2_best_strength
        nonlocal part2_best_length

        # part 1 max check
        if current_strength > part1_best_strength:
            part1_best_strength = current_strength

        # part 2 max check
        if len(visited_indices) >= part2_best_length and current_strength > part2_best_strength:
            part2_best_length = len(visited_indices)
            part2_best_strength = current_strength

        # Try adding all other pieces to current bridge
        for idx, piece in enumerate(input):
            # Check if we've already used this piece in the bridge
            if idx in visited_indices:
                continue

            piece_ports = [int(x) for x in piece.split('/')]

            # Check if piece matches the port we currently need
            if port_size in piece_ports:
                piece_strength = piece_ports[0] + piece_ports[1]
                next_port_size = piece_ports[1] if piece_ports[0] == port_size else piece_ports[0]
                visited_indices.add(idx)

                dfs(next_port_size, current_strength + piece_strength, visited_indices)

                # Backtrack when finished with DFS
                visited_indices.remove(idx)


    dfs(0, 0, set())

    print(f"Part 1: {part1_best_strength}, Part 2 (strength): {part2_best_strength}, Part 2 (length): {part2_best_length}")

    return part1_best_strength

def part2(input):
    best_strength = 0
    longest_bridge = 0

    # Try all combos and keep running tally of longest and best strength
    def dfs(port_size, current_strength, visited_indices):
        nonlocal longest_bridge
        nonlocal best_strength

        if len(visited_indices) >= longest_bridge and current_strength > best_strength:
            longest_bridge = len(visited_indices)
            best_strength = current_strength

        for idx, piece in enumerate(input):
            if idx in visited_indices:
                continue

            piece_ports = [int(x) for x in piece.split('/')]

            if port_size in piece_ports:
                piece_strength = piece_ports[0] + piece_ports[1]
                next_port_size = piece_ports[1] if piece_ports[0] == port_size else piece_ports[0]
                visited_indices.add(idx)

                dfs(next_port_size, current_strength + piece_strength, visited_indices)

                # Backtrack when finished with DFS
                visited_indices.remove(idx)


    dfs(0, 0, set())

    return best_strength


def main():
    # # Part 1 Example
    # input = open('/home/john/Documents/Projects/advent_of_code/2017/day24/example.txt', 'r').read().strip().split('\n')
    # result = part1(input)
    # print(f"Part 1 (example): {result}")

    # Part 1
    input = open('/home/john/Documents/Projects/advent_of_code/2017/day24/input.txt', 'r').read().strip().split('\n')
    result = part1(input)
    print(f"Part 1: {result}")

    # # Part 2 Example
    # input = open('/home/john/Documents/Projects/advent_of_code/2017/day24/example.txt', 'r').read().strip().split('\n')
    # result = part2(input)
    # print(f"Part 2 (example): {result}")

    # Part 2
    # input = open('/home/john/Documents/Projects/advent_of_code/2017/day24/input.txt', 'r').read().strip().split('\n')
    # result = part2(input)
    # print(f"Part 2: {result}")

main()