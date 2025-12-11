def part1(input):
    adjacency_map = parse_adjacency_map(input)
    result = dfs_part2('you', 'out', adjacency_map, {})
    return result


# DFS graph traversal with backtracking to find all paths from node to target
# Deprecated since part2's DFS can do both part 1 and 2
def dfs_part1(node, target, adjacency_map, seen_nodes):
    # Check if we've been here before
    if node in seen_nodes:
        return 0

    # Check if we found target
    if node == target:
        return 1

    # Drill baby, drill
    result = 0
    seen_nodes.add(node)
    for neighbor in adjacency_map[node]:
        if neighbor not in seen_nodes:
            result += dfs_part1(neighbor, target, adjacency_map, seen_nodes)

    # Backtrack and return
    seen_nodes.remove(node)
    return result

def part2(input):
    adjacency_map = parse_adjacency_map(input)

    # Route 1: SVR -> DAC -> FFT -> OUT
    # (Turns out there are 0 DAC->FFT paths, so this isn't actually necessary)
    svr_dac_paths = dfs_part2('svr', 'dac', adjacency_map, {})
    dac_fft_paths = dfs_part2('dac', 'fft', adjacency_map, {})
    fft_out_paths = dfs_part2('fft', 'out', adjacency_map, {})
    route1_paths = svr_dac_paths * dac_fft_paths * fft_out_paths

    # Route 2: SVR -> FFT -> DAC -> OUT
    svr_fft_paths = dfs_part2('svr', 'fft', adjacency_map, {})
    fft_dac_paths = dfs_part2('fft', 'dac', adjacency_map, {})
    dac_out_paths = dfs_part2('dac', 'out', adjacency_map, {})
    route2_paths = svr_fft_paths * fft_dac_paths * dac_out_paths
    
    return route1_paths + route2_paths

# DFS graph traversal with memoization to find all paths from node to target
def dfs_part2(node, target, adjacency_map, seen_nodes):
    # Check if we've been here before
    if node in seen_nodes:
        return seen_nodes[node]

    # Check if we found target
    if node == target:
        return 1
    
    # Check if we hit 'out' too early (bad path)
    if node == 'out':
        return 0

    # Drill baby, drill
    result = 0
    for neighbor in adjacency_map[node]:
        result += dfs_part2(neighbor, target, adjacency_map, seen_nodes)

    # Memoize and return
    seen_nodes[node] = result
    return result

def parse_adjacency_map(input):
    adjacency_map = {}
    # Parse input to a adjacency map
    for line in input:
        node, neighbors = line.strip().split(':')
        neighbors = neighbors.strip().split()
        adjacency_map[node] = set(neighbors)

    return adjacency_map

def main():
    part1_example_input = open('./example_part1.txt', 'r').read().split('\n')
    part2_example_input = open('./example_part2.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    part1_example_result = part1(part1_example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")

    # Part 2 Example
    part2_example_result = part2(part2_example_input)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2
    part2_result = part2(input)
    print(f"Part 2: {part2_result}")

main()