import heapq
from math import sqrt
from collections import deque

def part1(input, num_connections):
    distances = []

    # Calculate all distances between boxes
    # Only keep K closest neighbors for a box
    unique_distances = set([]) # If we computed the distance between box 1 and 2, don't compute distance between box 2 and 1
    num_closest_to_keep = 4 # Hard-coded via trial-and-error (sue me)
    for line1 in input:
        box1 = parse_box(line1)
        closest_neighbors = [] 
        for line2 in input:
            box2 = parse_box(line2)
            if box1 != box2:
                distance = get_distance(box1, box2)
                heapq.heappush(closest_neighbors, (distance, [box1, box2]))

        # Only keep track of the distances of the K closest neighbors
        for _ in range(num_closest_to_keep):
            distance, (box1, box2) = heapq.heappop(closest_neighbors)
            box_tuple = (min(box1, box2), max(box1, box2))
            if box_tuple not in unique_distances:
                unique_distances.add(box_tuple)
                heapq.heappush(distances, (distance, (box1, box2)))
        
    # Build graph of closest specified connections
    box_adjacencies = {}
    connections_made = 0
    part1_result = None
    part2_result = None
    while len(distances) > 0:
        distance, [box1_coordinates, box2_coordinates] = heapq.heappop(distances)

        # Connect the two boxes by updating their adjacency (even if they're already in the same circuit)
        box_adjacencies.setdefault(box1_coordinates, set()).add(box2_coordinates)
        box_adjacencies.setdefault(box2_coordinates, set()).add(box1_coordinates)

        # Part 2: Traverse box1's circuit and see if its size is the whole input
        subgraph_size, _ = traverse_circuit(box1_coordinates, box_adjacencies, set())
        if subgraph_size == len(input):
            part2_result = box1_coordinates[0] * box2_coordinates[0]
            return part1_result, part2_result

        # Part 1: Traverse circuits made so far and get their size
        if connections_made == num_connections - 1:
            seen_nodes = set()
            biggest_circuits = [] # This will be a max heap
            for box in box_adjacencies.keys():
                if box not in seen_nodes:
                    subgraph_size, seen_nodes = traverse_circuit(box, box_adjacencies, seen_nodes)
                    heapq.heappush(biggest_circuits, -subgraph_size) # To keep a max heap, make values negative


            # Multiply size of three biggest subgraphs
            part1_result = biggest_circuits[0] * biggest_circuits [1] * biggest_circuits[2] * -1 # Values are negative due to max heap
        
        connections_made += 1

    return part1_result, part2_result

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