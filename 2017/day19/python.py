def main():
    input = open('/home/john/Documents/Projects/advent_of_code/2017/day19/input.txt', 'r').readlines()

    current_row = 0
    current_column = 0
    current_char = '|'
    current_direction = 'down'
    part1_result = []
    part2_result = 0

    # find first pipe
    current_column = input[0].find('|')

    while current_char != ' ': # Path ends when we land on a blank space
        current_char = input[current_row][current_column]
        # Check for letter
        if current_char.isalpha():
            part1_result.append(current_char)
        # Check for corner
        elif current_char == '+':
            # changing direction
            if current_direction == 'up' or current_direction == 'down':
                # If we were going up or down, we should now go either left or right
                left = input[current_row][current_column - 1]
                right = input[current_row][current_column + 1]
                if left != ' ':
                    current_direction = 'left'
                elif right != ' ':
                    current_direction = 'right'
            elif current_direction == 'left' or current_direction == 'right':
                # If we were going left or right, we should now go either up or down
                up = input[current_row - 1][current_column]
                down = input[current_row + 1][current_column]
                if up != ' ':
                    current_direction = 'up'
                elif down != ' ':
                    current_direction = 'down'

        # Take one step in current direction
        if current_direction == 'down':
            current_row += 1
        elif current_direction == 'up':
            current_row -= 1
        elif current_direction == 'right':
            current_column += 1
        elif current_direction == 'left':
            current_column -= 1

        part2_result += 1

    print("".join(part1_result)) # Part 1
    print(part2_result - 1) # Part 2

main()