import heapq
from math import sqrt
from collections import deque

def part1(input, num_connections):
    distances = []

    # Calculate all distances between boxes
    unique_distances = set([])
    for idx1, line1 in enumerate(input):
        box1 = parse_box(line1)
        for idx2, line2 in enumerate(input):
            # Don't compute the distance between a box and itself
            if idx1 == idx2:
                continue

            # Check if we've already computed the distance between these two boxes
            box_tuple = (min(idx1, idx2), max(idx1, idx2))
            if box_tuple in unique_distances:
                continue
            else:
                unique_distances.add(box_tuple)

            # Compute distance between boxes
            box2 = parse_box(line2)
            distance = get_distance(box1, box2)
            distances.append((distance, [(idx1, box1), (idx2, box2)]))

    # Order distances
    heapq.heapify(distances)

    # Build graph of closest specified connections
    box_adjacencies = {}
    connections_made = 0
    part1_result = None
    while True:
        distance, [(box1_idx, box1_coordinates), (box2_idx, box2_coordinates)] = heapq.heappop(distances)

        # Update box1 adjacency
        if box1_idx not in box_adjacencies:
            box_adjacencies[box1_idx] = set([box2_idx])
        else:
            box_adjacencies[box1_idx].add(box2_idx)

        # Update box2 adjacency
        if box2_idx not in box_adjacencies:
            box_adjacencies[box2_idx] = set([box1_idx])
        else:
            box_adjacencies[box2_idx].add(box1_idx)

        # Part 2: Traverse box1's circuit and see if its size is the whole input
        subgraph_size, _ = traverse_circuit(box1_idx, box_adjacencies, set())
        if subgraph_size == len(input):
            part2_result = box1_coordinates[0] * box2_coordinates[0]
            return part1_result, part2_result

        # Part 1: Traverse circuits made so far and get their size
        if connections_made == num_connections - 1:
            seen_nodes = set()
            biggest_circuits = []
            for box in box_adjacencies.keys():
                if box not in seen_nodes:
                    subgraph_size, seen_nodes = traverse_circuit(box, box_adjacencies, seen_nodes)
                    heapq.heappush(biggest_circuits, -subgraph_size) # To keep a max heap, make values negative


            # Multiply size of three biggest subgraphs
            part1_result = biggest_circuits[0] * biggest_circuits [1] * biggest_circuits[2] * -1 # Values are negative due to max heap
        
        connections_made += 1


def parse_box(input_line):
    box_x, box_y, box_z = input_line.split(',')
    return (int(box_x), int(box_y), int(box_z))

def get_distance(box1, box2):
    x_distance = (box2[0] - box1[0]) ** 2
    y_distance = (box2[1] - box1[1]) ** 2
    z_distance = (box2[2] - box1[2]) ** 2
    return round(sqrt(x_distance + y_distance + z_distance), 3)


def traverse_circuit(node, adjacency_map, seen_nodes):
    # BFS to traverse a circuit
    queue = deque()
    queue.append(node)
    circuit_size = 0

    while len(queue) > 0:
        node = queue.popleft()
        if node not in seen_nodes:
            seen_nodes.add(node)
            circuit_size += 1
            
            # Queue up neighbors to be visited
            for neighbor in adjacency_map[node]:
                if neighbor not in seen_nodes:
                    queue.append(neighbor)

    return circuit_size, seen_nodes

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 & 2 Example
    part1_example_result, part2_example_result = part1(example_input, 10)
    print(f"Part 1 (example): {part1_example_result}")
    print(f"Part 2 (example): {part2_example_result}")

    # Part 1 & 2
    part1_result, part2_result = part1(input, 1000)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

main()