import heapq

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

    # Part 1 & 2 Example
    part1_example_result, part2_example_result = part2_union_find(example_input, 10)
    print(f"Part 1 (example): {part1_example_result}")
    print(f"Part 2 (example): {part2_example_result}")

    # Part 1 & 2
    part1_result, part2_result = part2_union_find(input, 1000)
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

main()