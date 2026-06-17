import math

goal = (2, 2)
moves = [(0,1),(1,0),(-1,0),(0,-1)]

def heuristic(pos):
    return - (abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]))

def is_goal(pos):
    return pos == goal

def minimax(pos, opponent, depth, maximizing):
    if (depth == 0 or is_goal(pos)):
        h = heuristic(pos)
        print(" Leaf Node :", pos, " Heuristic :", h)
        return h
    if (maximizing):
        max_eval = -math.inf
        for m in moves:
            new_pos = (pos[0]+m[0], pos[1]+m[1])
            eval = minimax(new_pos, opponent, depth-1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for m in moves:
            new_opp = (opponent[0]+m[0], opponent[1]+m[1])
            eval = minimax(pos, new_opp, depth-1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(pos, opponent, depth):
    best_val = -math.inf
    best = None
    for m in moves:
        new_pos = (pos[0]+m[0], pos[1]+m[1])
        val = minimax(new_pos, opponent, depth-1, False)
        print(" Move:", m, "Value:", val)
        if (val > best_val):
            best_val = val
            best = m
    print(" Chosen Move:", best)
    return best

states = [((0,0),(1,1)), ((1,0),(0,2)), ((0,1),(2,0))]

for s in states:
    print(" State :", s)
    print(" Depth 2")
    best_move(s[0], s[1], 2)
    print(" Depth 3")
    best_move(s[0], s[1], 3)
