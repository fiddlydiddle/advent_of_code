import heapq
from collections import deque

def part2(input, num_connections):

    # Calculate all distances between boxes
    distances = calc_distances(input)

    # Build graph of closest specified connections
    box_adjacencies = {} # Keep track each box's connections
    circuit_sizes = {} # Keep track of each box's circuit size
    connections_made = 0
    part1_result = None
    part2_result = None
    while len(distances) > 0:
        _, [box1_coordinates, box2_coordinates] = heapq.heappop(distances)

        box1_circuit_size = circuit_sizes.get(box1_coordinates, 0)
        box2_circuit_size = circuit_sizes.get(box2_coordinates, 0)
        
        # Check if boxes are already in the same circuit BEFORE connecting them
        are_in_same_circuit = False
        if box1_circuit_size > 0 and box1_circuit_size == box2_circuit_size:
            are_in_same_circuit, _ = traverse_circuit(box1_coordinates, box_adjacencies, set(), box2_coordinates)

        # Connect the two boxes by updating their adjacency (even if they're already in the same circuit)
        box_adjacencies.setdefault(box1_coordinates, set()).add(box2_coordinates)
        box_adjacencies.setdefault(box2_coordinates, set()).add(box1_coordinates)

        connections_made += 1
        if connections_made == num_connections:
            # We've made the number of connections specified in part 1, calc part 1 result
            part1_result = part1(box_adjacencies)

        # Can skip part 2's traversale if the two boxes were already in the same circuit
        # They're connection won't make the circuit bigger since they're already connected
        if are_in_same_circuit:
            continue
        
        # Part 2: Traverse box1's circuit and see if its size is the whole input
        subgraph_size, newly_seen_boxes = traverse_circuit(box1_coordinates, box_adjacencies, set())
        for box in newly_seen_boxes:
            circuit_sizes[box] = subgraph_size

        if subgraph_size == len(input):
            part2_result = box1_coordinates[0] * box2_coordinates[0]
            return part1_result, part2_result

        
        
    return part1_result, part2_result

def part1(box_adjacencies):
    # Go through each box in the adjacency graph and traverse its circuit
    seen_boxes = set()
    biggest_circuits = []
    for box in box_adjacencies.keys():
        if box not in seen_boxes:
            subgraph_size, seen_boxes = traverse_circuit(box, box_adjacencies, seen_boxes)
            heapq.heappush(biggest_circuits, -subgraph_size) # To keep a max heap, make values negative

    # Multiply size of three biggest subgraphs
    return biggest_circuits[0] * biggest_circuits [1] * biggest_circuits[2] * -1 # Values are negative due to max heap

def calc_distances(input):
    distances = [] # This will be a minheap to keep the distances sorted as we go
    unique_tuples = set([])
    for line1 in input:
        box1 = parse_box(line1)
        for line2 in input:
            box2 = parse_box(line2)
            # Don't compute the distance between a box and itself
            if box1 == box2:
                continue

            # Check if we've already computed the distance between these two boxes
            box_tuple = (min(box1, box2), max(box1, box2))
            if box_tuple in unique_tuples:
                continue
            else:
                unique_tuples.add(box_tuple)

            # Compute distance between boxes
            distance = get_distance(box1, box2)
            heapq.heappush(distances, (distance, [box1, box2]))

    return distances


def traverse_circuit(start_box, adjacency_map, seen_boxes, target_box=None):
    # BFS to traverse a circuit, optionally stopping when finding a target box
    seen_boxes_copy = set() if target_box else seen_boxes
    queue = deque()
    queue.append(start_box)
    circuit_size = 0

    while len(queue) > 0:
        box = queue.popleft()
        if box not in seen_boxes_copy:
            seen_boxes_copy.add(box)
            circuit_size += 1
            
            # Queue up neighbors to be visited
            for neighbor in adjacency_map[box]:
                if neighbor == target_box:
                    # We found the specified target
                    return True, None
                if neighbor not in seen_boxes_copy:
                    queue.append(neighbor)

    if target_box:
        # We were searching for a target, but didn't find it
        return False, None

    # We weren't searching for a target, but just traversing the circuit
    return circuit_size, seen_boxes_copy


def parse_box(input_line):
    box_x, box_y, box_z = input_line.split(',')
    return (int(box_x), int(box_y), int(box_z))


def get_distance(box1, box2):
    x_distance = (box2[0] - box1[0]) ** 2
    y_distance = (box2[1] - box1[1]) ** 2
    z_distance = (box2[2] - box1[2]) ** 2
    return x_distance + y_distance + z_distance

################################
# AI- Generated
################################
def part2_union_find(input, num_connections):
    # --- 1. Union-Find Initialization ---
    
    # Calculate all distances between boxes
    distances = calc_distances_optimized(input)
    
    # Store parent of each box (initially each box is its own parent)
    parent = {}
    # Store size of each component (initially each box's component size is 1)
    size = {} 
    
    # Initialize all unique boxes from the input
    unique_boxes = set()
    for line in input:
        box = parse_box(line)
        unique_boxes.add(box)
        parent[box] = box
        size[box] = 1

    # --- 2. Core Union-Find Functions ---

    def find(box):
        # Path compression: makes future lookups faster
        if parent[box] == box:
            return box
        parent[box] = find(parent[box])
        return parent[box]

    def union(box1, box2):
        # Find representatives
        root1 = find(box1)
        root2 = find(box2)

        # Already in the same circuit
        if root1 == root2:
            return False, size[root1] # Returns False for "no merge" and the current size

        # Union by size (make the smaller tree point to the larger tree)
        if size[root1] < size[root2]:
            root1, root2 = root2, root1 # Swap so root1 is always the larger/equal component

        # Merge: root2 component is attached to root1
        parent[root2] = root1
        size[root1] += size[root2]
        
        # Returns True for "merge occurred" and the new size
        return True, size[root1]

    # --- 3. Kruskal's Algorithm with Union-Find ---

    connections_made = 0
    part1_result = None
    
    # We need a separate structure to store the edges for Part 1's calculation
    # as Union-Find doesn't inherently store the graph structure.
    part1_adjacencies = {} 
    
    while distances:
        distance, [box1, box2] = heapq.heappop(distances)
        
        # Attempt to merge the circuits containing box1 and box2
        merged, current_size = union(box1, box2)

        # --- Part 1 Tracking ---
        
        # Add the connection to the graph structure needed for part1()
        part1_adjacencies.setdefault(box1, set()).add(box2)
        part1_adjacencies.setdefault(box2, set()).add(box1)

        connections_made += 1
        if connections_made == num_connections:
            # We must convert the Union-Find components into the structure part1 expects
            part1_result = part1_union_find_helper(parent, size)

        # --- Part 2 Check ---
        
        # Only check if a merge occurred, as the size only increases during a merge
        if merged:
            # Check if the single, massive circuit is complete
            if current_size == len(unique_boxes):
                # The connection that completed the circuit is the edge (box1, box2)
                part2_result = box1[0] * box2[0]
                return part1_result, part2_result

    return part1_result, None


def part1_union_find_helper(parent, size):
    # Uses the Union-Find results (parent/size maps) to find the top 3 biggest components.
    
    # 1. Collect all component sizes by looking at the roots
    biggest_circuits = []
    
    # The 'size' map only contains sizes for the representative roots.
    for box in parent.keys():
        if parent[box] == box: # Check if the box is a root/representative
            heapq.heappush(biggest_circuits, -size[box]) # Push negative size for max heap

    # 2. Extract and multiply the size of three biggest subgraphs
    if len(biggest_circuits) < 3:
        # Handle case where there aren't 3 separate components (shouldn't happen for AoC)
        return 0 
        
    size1 = -heapq.heappop(biggest_circuits)
    size2 = -heapq.heappop(biggest_circuits)
    size3 = -heapq.heappop(biggest_circuits)
    
    return size1 * size2 * size3

def calc_distances_optimized(input):
    distances_heap = []
    parsed_boxes = [parse_box(line) for line in input]
    
    # Track unique edges we've already processed (tuple of (min_box, max_box))
    unique_edges = set() 
    
    # Choose a small, arbitrary K value (e.g., 5 or 10)
    K = 5

    for i, box1 in enumerate(parsed_boxes):
        # Use a temporary heap to find the K smallest distances for box1
        k_closest_distances = [] 
        
        for j, box2 in enumerate(parsed_boxes):
            if box1 == box2:
                continue

            distance = get_distance(box1, box2)
            
            # Use a max-heap of size K to efficiently track the smallest K distances
            # We push the negative distance because Python's heapq is a min-heap.
            if len(k_closest_distances) < K:
                heapq.heappush(k_closest_distances, (-distance, [box1, box2]))
            elif -distance > k_closest_distances[0][0]: # Check if new distance is smaller than the current largest in the heap
                heapq.heapreplace(k_closest_distances, (-distance, [box1, box2]))

        # Add the K-closest edges to the main distances heap, handling uniqueness
        for neg_dist, edge in k_closest_distances:
            box_tuple = (min(edge), max(edge))
            if box_tuple not in unique_edges:
                unique_edges.add(box_tuple)
                # Note: We must negate neg_dist back to a positive distance
                heapq.heappush(distances_heap, (-neg_dist, edge))
                
    return distances_heap

################################
# /AI-Generated
################################

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # # Part 1 & 2 Example
    # part1_example_result, part2_example_result = part2(example_input, 10)
    # print(f"Part 1 (example): {part1_example_result}")
    # print(f"Part 2 (example): {part2_example_result}")

    # Part 1 & 2
    part1_result, part2_result = part2(input, 1000)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

    # # Part 1 & 2 (Union Find)
    # part1_result, part2_result = part2_union_find(input, 1000)
    # print(f"Part 1: {part1_result}")
    # print(f"Part 2: {part2_result}")

main()