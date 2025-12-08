from functools import reduce

def part1(input):
    result = 0
    current_col_idx = 0
    col_height = len(input)

    # Parse the input into columns of values
    parsed_input = []
    for line in input:
        line = line.strip().split()
        parsed_input.append(line)

    # Move through input column-by-column and do the maths
    while current_col_idx < len(parsed_input[0]):
        operator = parsed_input[col_height - 1][current_col_idx]

        # Initialize running_total to identity element for column's operation
        running_total = 0
        if operator == '*':
            running_total = 1

        # Total up the column
        for row_idx in range(col_height - 1):
            if operator == '*':
                running_total *= int(parsed_input[row_idx][current_col_idx])
            else:
                running_total += int(parsed_input[row_idx][current_col_idx])

        # Add to total value, move to next column
        result += running_total
        current_col_idx += 1


    return result

def part2(input):
    result = 0
    col_height = len(input) - 1

    # Determine the column widths by looking at the operator row (the last row)
    # The width of a column is the difference between its operator and the next operator - 1
    col_info = []
    col_idx = 0
    operation_idx = -1
    operation_width = 0
    operation = '+'
    while col_idx < len(input[0]):
        if input[col_height][col_idx] in "+*":
            # Found next operation, record width of previous operation
            if operation_idx >= 0:
                col_info.append((operation_width - 1, operation))

            operation_idx += 1
            operation_width = 0
            operation = input[col_height][col_idx]

        operation_width += 1
        col_idx += 1
    col_info.append((operation_width, operation))

    # Now that we know how wide each column of operations is we can iterate through
    # Build each value, increment a running total, then add to result
    col_padding = 0
    for col_width, operation in col_info:
        # Initialize the running total to the identity element for the column's operation
        running_total = 0 if operation == '+' else 1
        for col_idx in range(col_width):

            # Starting from top of column and moving down append each value we see to the column's value
            col_value = 0
            for row_idx in range(col_height):
                digit = input[row_idx][col_idx + col_padding]
                if digit != ' ':
                    # If there is a digit we need to append it in a math-y way
                    col_value *= 10
                    col_value += int(digit)
            
            if operation == "+":
                running_total += col_value
            else:
                running_total *= col_value

        result += running_total
        col_padding += col_width + 1

    return result

################
# AI Generated  
################  
class LogicalTranspose:
    def __init__(self, lines):
        self.lines = lines
        self.nrows = len(lines)
        self.ncols = max(len(line) for line in lines) if lines else 0
    
    def get_row(self, row_idx):
        """Get a transposed row (which is a column in the original)"""
        result = ""
        for col_idx in range(self.nrows):
            if row_idx < len(self.lines[col_idx]):
                result += self.lines[col_idx][row_idx]
            else:
                result += " "
        return result
    
    def __iter__(self):
        """Iterate through transposed rows"""
        for row_idx in range(self.ncols):
            yield self.get_row(row_idx)
    
    def __len__(self):
        return self.ncols


def part2_transpose(input):
    # Create logical transpose - no mutation of input
    transposed = LogicalTranspose(input[:-1])
    
    operators = input[-1].split()
    
    total = 0
    i_problem = 0
    operands = []
    # Iterate through transposed rows plus one empty row at the end
    for line in list(transposed):
        if len(line.strip()) == 0:
            if operands:  # Only process if we have operands
                operator = operators[i_problem]
                if operator == "+":
                    total += sum(operands)
                else:
                    total += reduce(lambda curr, new: curr * new, operands, 1)
                
                i_problem += 1
                operands = []
        else:
            operands.append(int(line))
    
    return total

################
# /AI Generated  
################ 


def main():
    example_input = open('./example.txt', 'r').read().split('\n')
    input = open('./input.txt', 'r').read().split('\n')

    # Part 1 Example
    result = part1(example_input)
    print(f"Part 1 (example): {result}")

    # Part 1
    result = part1(input)
    print(f"Part 1: {result}")

    # Part 2 Example
    result = part2(example_input)
    print(f"Part 2 (example): {result}")

    # Part 2
    result = part2(input)
    print(f"Part 2: {result}")

main()