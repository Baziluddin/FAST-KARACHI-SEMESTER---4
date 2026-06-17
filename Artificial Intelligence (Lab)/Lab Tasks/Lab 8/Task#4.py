import math

board = [" "]*9

def print_board():
    for i in range(0,9,3):
        print(board[i:i+3])

def check_winner(b):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for w in wins:
        if (b[w[0]] == b[w[1]] == b[w[2]] != " "):
            return b[w[0]]
    if " " not in b:
        return "D"
    return None

nodes = 0
pruned = 0

def alphabeta(b, depth, alpha, beta, maximizing):
    global nodes, pruned
    nodes += 1
    result = check_winner(b)
    if (result == "X"):
        return 10 - depth
    if (result == "O"):
        return depth - 10
    if (result == "D"):
        return 0

    if maximizing:
        max_eval = -math.inf
        for i in range(9):
            if (b[i] == " "):
                b[i] = "X"
                eval = alphabeta(b, depth+1, alpha, beta, False)
                b[i] = " "
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if (beta <= alpha):
                    pruned += 1
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if (b[i] == " "):
                b[i] = "O"
                eval = alphabeta(b, depth+1, alpha, beta, True)
                b[i] = " "
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if (beta <= alpha):
                    pruned += 1
                    break
        return min_eval

def best_move():
    best_val = -math.inf
    move = None
    for i in range(9):
        if (board[i] == " "):
            board[i] = "X"
            val = alphabeta(board, 0, -math.inf, math.inf, False)
            board[i] = " "
            if (val > best_val):
                best_val = val
                move = i
    return move

while True:
    m = best_move()
    board[m] = "X"
    print(" AI Move:")
    print_board()

    if check_winner(board):
        break

    h = int(input("Enter move (0-8): "))
    if (board[h] == " "):
        board[h] = "O"

    if check_winner(board):
        break

print(" Final Board :")
print_board()
print(" Result :", check_winner(board))
print(" Nodes explored :", nodes)
print(" Pruned branches :", pruned)
