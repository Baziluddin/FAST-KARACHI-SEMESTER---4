def validCheck(board, row, col, num):
    for i in range(6):
        if (board[row][i] == num):
            return False
        if (board[i][col] == num):
            return False

    sr = (row // 2) * 2
    sc = (col // 3) * 3

    for i in range(2):
        for j in range(3):
            if (board[sr + i][sc + j] == num):
                return False

    return True

def solve(board):
    for i in range(6):
        for j in range(6):
            if (board[i][j] == 0):
                for num in range(1, 7):
                    if (validCheck(board, i, j, num)):
                        board[i][j] = num
                        if (solve(board)):
                            return True
                        board[i][j] = 0
                return False
    return True

board = [
    [0, 0, 6, 2, 0, 5],
    [0, 0, 0, 4, 6, 0],
    [0, 1, 2, 0, 0, 0],
    [5, 6, 0, 0, 0, 4],
    [0, 0, 4, 3, 0, 2],
    [3, 0, 0, 5, 0, 6]
]

if solve(board):
    for row in board:
        print(row)
else:
    print("NoSolution")
