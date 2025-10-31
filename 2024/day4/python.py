def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2024/day4/input.txt', 'r').readlines()
    part1_result = part1(input)
    print(f"Part 1: {part1_result}")
    part2_result = part2(input)
    print(f"Part 2: {part2_result}")

def part2(input):
    result = 0
    width = len(input[0]) - 1 # Input contains newline characters on each line
    height = len(input)

    for i in range(height - 2):
        for j in range(width - 2):
            if (input[i][j] == "M" or input[i][j] == "S"):
                if has_x_mas(input, i, j):
                    result += 1
    
    return result

def has_x_mas(input, row, col):
    start_letter = input[row][col]
    end_letter = "S" if start_letter == "M" else "M"
    
    if input[row + 1][col + 1] != "A":
        return False

    if input[row + 2][col + 2] != end_letter:
        return False
    
    other_cross_start_letter = input[row][col + 2]
    if other_cross_start_letter != "S" and other_cross_start_letter != "M":
        return False
    
    other_cross_end_letter = "S" if other_cross_start_letter == "M" else "M"
    if input[row + 2][col] != other_cross_end_letter:
        return False
    
    return True
    

def part1(input):
    result = 0
    width = len(input[0]) - 1 # Input contains newline characters on each line
    height = len(input)

    # Horizontal search
    for line in input:
        result += line.count('XMAS')
        result += line.count('SAMX')

    # Vertical search, build vertical slices
    slices = []
    for i in range(width):
        slice = ''
        for j in range(height):
            slice += input[j][i]
        slices.append(slice)

    for slice in slices:
        result += slice.count('XMAS')
        result += slice.count('SAMX')

    # Diagonal search (top left to bottom right), build diagonal slices
    row_idx = len(input) - 1
    slices = []
    while row_idx >= 0:
        slice = ''
        col_idx = 0
        row_offset = 0
        while col_idx < width and row_idx + row_offset < height:
            slice += input[row_idx + row_offset][col_idx]
            col_idx += 1
            row_offset += 1
        
        slices.append(slice)
        row_idx -= 1

    col_idx = 1
    while col_idx < width:
        slice = ''
        row_idx = 0
        col_offset = 0
        while row_idx < height and col_idx + col_offset < width:
            slice += input[row_idx][col_idx + col_offset]
            row_idx += 1
            col_offset += 1
        
        slices.append(slice)
        col_idx += 1

    for slice in slices:
        result += slice.count('XMAS')
        result += slice.count('SAMX')

    # Diagonal search (top right to bottom left), build diagonal slices
    row_idx = len(input) - 1
    slices = []
    while row_idx >= 0:
        slice = ''
        col_idx = width - 1
        row_offset = 0
        while col_idx >= 0 and row_idx + row_offset < height:
            slice += input[row_idx + row_offset][col_idx]
            col_idx -= 1
            row_offset += 1
        
        slices.append(slice)
        row_idx -= 1

    col_idx = width - 2
    while col_idx >= 0:
        slice = ''
        row_idx = 0
        col_offset = 0
        while row_idx < height and col_idx + col_offset >= 0:
            slice += input[row_idx][col_idx + col_offset]
            row_idx += 1
            col_offset -= 1
        
        slices.append(slice)
        col_idx -= 1

    for slice in slices:
        result += slice.count('XMAS')
        result += slice.count('SAMX')

    return result


main()