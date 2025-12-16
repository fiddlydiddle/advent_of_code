class ParsedInput:
    def __init__(self, shapes, regions):
        self.shapes = shapes
        self.regions = regions

class Region:
    def __init__(self, x_dimension, y_dimension, required_shapes):
        self.x_dimension = int(x_dimension)
        self.y_dimension = int(y_dimension)
        self.required_shapes = required_shapes

class Shape:
    def __init__(self, cells):
        self.cells = sorted(cells)
        self.is_flipped = False
        self.num_rotations = 0

    def rotate(self):
        self.num_rotations = (self.num_rotations + 1) % 4

    def flip(self):
        self.is_flipped = not self.is_flipped

    def get_cells(self):
        transformed_cells = self.cells

        # Apply flips and rotations transformation in a single pass
        final_cells = []
        for x, y in transformed_cells:
            if self.is_flipped:
                x, y = -x, y
            
            if self.num_rotations == 1:
                x, y = -y, x
            elif self.num_rotations == 2:
                x, y = -x, -y
            elif self.num_rotations == 3:
                x, y = y, -x

            final_cells.append((x, y))

        # Fix negative indices 
        min_x = min(x for x, y in final_cells)
        min_y = min(y for x, y in final_cells)
        slide_x = -min_x
        slide_y = -min_y
        bounded_cells = [(x + slide_x, y + slide_y) for x, y in final_cells]

        return sorted(bounded_cells)


def part1(input):
    good_regions = 0
    for idx, region in enumerate(input.regions):
        # Grid is set of availalble cells in the region
        # As we put pieces into the region we will remove the corresponding cells from th grid
        region_area = region.x_dimension * region.y_dimension

        # Wait let's just check if the required pieces could even potentially fit regardless of their shapes
        # It can't be that easy, right? RIGHT?!
        piece_area = 0
        for shape in region.required_shapes:
            piece_area += len(shape.get_cells())

        if piece_area <= region.x_dimension * region.y_dimension:
            good_regions += 1

    # I can't believe that f@#king WORKED!
    return good_regions

# Not finished, trying something else
def dfs_place_shape(shapes, grid):
    # Take first remaining shape to place
    # Flip and roa
    shape = shapes[0]
    for _ in range(2):
        shape.flip()
        for _ in range(4):
            shape.rotate()
            cells = shape.get_cells()
            for available_space in grid:
                space_row, space_col = available_space
                shape_fits = True
                # Try to put flipped/rotated shape in grid
                for cell_row, cell_col in cells:
                    cell_placement_row = cell_row + space_row
                    cell_placement_col = cell_col + space_col
                    
                    if (cell_placement_row, cell_placement_col) not in grid:
                        # Doesn't fit
                        shape_fits = False
                        break

                # It fit!
                if shape_fits:
                    return True
                
    # No combination of flips/rotations fit
    return False

def parse_input(input):
    shapes = []
    regions = []

    parsing_shapes = True
    current_shape = []
    current_shape_row = 0
    for line in input:
        # We've hit the "regions" section of input once we see a line with an 'x'
        if 'x' in line:
            parsing_shapes = False

        if parsing_shapes:
            # Each shape ends with a blank line
            if line.strip() == '':
                current_shape = sorted(current_shape)
                shapes.append(Shape(current_shape))
                current_shape = []
                current_shape_row = 0
            elif ':' not in line:
                for col_idx, char in enumerate(line):
                    if char == '#':
                        current_shape.append((current_shape_row, col_idx))
                current_shape_row += 1
        else:
            # Parsing the regions section of the input
            dimensions, required_shapes = line.strip().split(':')
            x_dimension, y_dimension = dimensions.split('x')
            required_shapes_nums = required_shapes.strip().split()
            required_shapes = []
            for idx in range(len(required_shapes_nums)):
                for _ in range(int(required_shapes_nums[idx])):
                    required_shapes.append(shapes[idx])
            regions.append(Region(x_dimension, y_dimension, required_shapes))

    return ParsedInput(shapes, regions)


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    parsed_example_input = parse_input(example_input)
    input = open('./input.txt', 'r').read().split('\n')
    parsed_input = parse_input(input)

    # Part 1 Example
    part1_example_result = part1(parsed_example_input)
    print(f"Part 1 (example): {part1_example_result}")

    # Part 1
    part1_result = part1(parsed_input)
    print(f"Part 1: {part1_result}")


main()