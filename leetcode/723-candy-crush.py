def main(board):
    current_board = board
    while True:
        # crush_board will return None when there are no changes to be made
        new_board = crush_board(current_board)
        if not new_board:
            return current_board
        else:
            current_board = new_board
    
def crush_board(board):
    spaces_to_crush = set()

    # Check for row-wise spaces to crush
    for row_idx, row in enumerate(board):
        left = 0
        right = 0
        streak_spaces = set()

        while right < len(row):
            if row[right] != row[left] or row[right] == 0:
                if len(streak_spaces) >= 3:
                    spaces_to_crush.update(streak_spaces)
                left = right
                streak_spaces.clear()
                
            streak_spaces.add((row_idx, right))
            right += 1

        if len(streak_spaces) >= 3:
            spaces_to_crush.update(streak_spaces)

    # Check for column-wise spaces to crush
    for col_idx in range(len(board[0])):
        left = 0
        right = 0
        streak_spaces = set()

        while right < len(board):
            if board[right][col_idx] != board[left][col_idx] or board[right][col_idx] == 0:
                if len(streak_spaces) >= 3:
                    spaces_to_crush.update(streak_spaces)
                left = right
                streak_spaces.clear()
                
            streak_spaces.add((right, col_idx))
            right += 1

        if len(streak_spaces) >= 3:
            spaces_to_crush.update(streak_spaces)

    if len(spaces_to_crush) == 0:
        return None
    
    # shift remaining pieces to fill the space
    new_board = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    height = len(board)
    for col_idx in range(len(board[0])):
        insert_row = height - 1
        for row_idx in range(len(board) - 1, -1, -1):
            if (row_idx, col_idx) not in spaces_to_crush:
                new_board[insert_row][col_idx] = board[row_idx][col_idx]
                insert_row -= 1


    return new_board


def tests():
    test1_input = [
        [110,5  ,112,113,114],
        [210,211,5  ,213,214],
        [310,311,3  ,313,314],
        [410,411,412,5  ,414],
        [5  ,1  ,512,3  ,3  ],
        [610,4  ,1  ,613,614],
        [710,1  ,2  ,713,714],
        [810,1  ,2  ,1  ,1  ],
        [1  ,1  ,2  ,2  ,2  ],
        [4  ,1  ,4  ,4  ,1014]
    ]
    result = main(test1_input)
    print(result)

    test2_input = [
        [1,3,5,5,2],
        [3,4,3,3,1],
        [3,2,4,5,2],
        [2,4,4,5,5],
        [1,4,4,1,1]
    ]
    result = main(test2_input)
    print(result)
tests()