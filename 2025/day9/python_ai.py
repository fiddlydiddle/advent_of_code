import math
from collections import defaultdict

def part2_optimized(input_lines):
    red_tiles = []
    # 1. Parse Red Tiles
    for line in input_lines:
        if not line.strip():
            continue
        y_str, x_str = line.split(',') 
        x, y = int(x_str), int(y_str)
        red_tiles.append((x, y))

    if not red_tiles:
        return 0
    
    num_red_tiles = len(red_tiles)
    red_tile_set = set(red_tiles)
    
    # 2. Pre-process boundary segments for efficient checking
    vertical_segments = defaultdict(list)  # {x: [(y_min, y_max), ...]}
    horizontal_segments = defaultdict(list)  # {y: [(x_min, x_max), ...]}
    
    for i in range(num_red_tiles):
        P1 = red_tiles[i]
        P2 = red_tiles[(i + 1) % num_red_tiles]
        x1, y1 = P1
        x2, y2 = P2
        
        if x1 == x2:  # Vertical edge
            y_min, y_max = min(y1, y2), max(y1, y2)
            vertical_segments[x1].append((y_min, y_max))
        elif y1 == y2:  # Horizontal edge
            x_min, x_max = min(x1, x2), max(x1, x2)
            horizontal_segments[y1].append((x_min, x_max))
    
    # 3. Point-in-polygon test using ray casting with caching
    point_cache = {}
    
    def is_valid_point(x, y):
        """Check if point is red or green (on boundary or inside polygon)."""
        if (x, y) in point_cache:
            return point_cache[(x, y)]
        
        # Check if it's a red tile
        if (x, y) in red_tile_set:
            point_cache[(x, y)] = True
            return True
        
        # Check if on boundary (green edge tiles) - fast check
        if x in vertical_segments:
            for y_min, y_max in vertical_segments[x]:
                if y_min <= y <= y_max:
                    point_cache[(x, y)] = True
                    return True
        if y in horizontal_segments:
            for x_min, x_max in horizontal_segments[y]:
                if x_min <= x <= x_max:
                    point_cache[(x, y)] = True
                    return True
        
        # Check if inside using ray casting
        intersections = 0
        for i in range(num_red_tiles):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[(i + 1) % num_red_tiles]
            
            # Skip horizontal edges (already checked above)
            if y1 == y2:
                continue
            
            # Check if ray from (x, y) going right intersects this edge
            if (y1 > y) != (y2 > y):  # Ray crosses the edge's y-range
                x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if x_intersect > x:
                    intersections += 1
        
        result = intersections % 2 == 1
        point_cache[(x, y)] = result
        return result
    
    # 4. Efficient rectangle validation with early termination
    def is_valid_rectangle(x1, y1, x2, y2):
        """Check if rectangle with opposite corners (x1,y1) and (x2,y2) is valid."""
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)
        
        # Fast filter: Check if any boundary segment cuts through the interior
        # Check vertical segments
        for x_seg, segments in vertical_segments.items():
            if x_min < x_seg < x_max:  # Segment cuts through interior
                for y_min_seg, y_max_seg in segments:
                    if y_min_seg < y_max and y_max_seg > y_min:
                        return False
        
        # Check horizontal segments
        for y_seg, segments in horizontal_segments.items():
            if y_min < y_seg < y_max:  # Segment cuts through interior
                for x_min_seg, x_max_seg in segments:
                    if x_min_seg < x_max and x_max_seg > x_min:
                        return False
        
        # Check all four corners (must be valid)
        # corners = [(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)]
        # for cx, cy in corners:
        #     if not is_valid_point(cx, cy):
        #         return False
        
        # If corners are valid and no segments cut through, rectangle is valid
        # (We can skip checking every interior point because of the segment check)
        return True
    
    # 5. Find largest rectangle
    max_area = 0
    
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            
            # Skip if the area is 0
            if x1 == x2 or y1 == y2:
                continue
            
            if is_valid_rectangle(x1, y1, x2, y2):
                # Area is calculated inclusively (count all tiles including corners)
                current_area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                max_area = max(max_area, current_area)
    
    return max_area

# Example usage (assuming you have the input lines loaded)
# input_data = ["7,1", "11,1", "11,7", "9,7", "9,5", "2,5", "2,3", "7,3"]
# result = part2_optimized(input_data)
# print(f"Largest area: {result}")

def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 2 Example
    part2_example_result = part2_optimized(example_input)
    print(f"Part 2 (example): {part2_example_result}")

    # Part 2
    part2_result = part2_optimized(input)
    print(f"Part 2: {part2_result}")


main()