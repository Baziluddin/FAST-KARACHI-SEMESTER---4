
from collections import (deque)

start = ((7,2,4),
         (5,0,6),
         (8,3,1))

goal = ((0,1,2),
        (3,4,5),
        (6,7,8))

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def neighbors(state):
    moves = []
    x, y = find_blank(state)
    directions = [(1,0),(-1,0),(0,1),(0,-1)]

    for dx, dy in directions:
        nx,ny = x+dx,  y+dy
        if (0 <= nx < 3 and 0 <= ny < 3):
            new_state = [list(row) for row in state]
            new_state[x][y],new_state[nx][ny] = new_state[nx][ny],new_state[x][y]
            moves.append(tuple(tuple(row) for row in new_state))

    return moves

def Bfs_puzzle(start, goal):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()

        if (state == goal):
            return path + [state]

        visited.add(state)

        for next_state in neighbors(state):
            if next_state not in visited:
                queue.append((next_state, path + [state]))

    return None


print(Bfs_puzzle(start,goal))
