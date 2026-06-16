maze = [
    ['S', 0, 0, 1, 0],
    [1, 0, 1, 0, 0],
    [0, 0, 0, 0, 'G'],
    [1, 1, 0, 1, 1]
]
rows = len(maze)
cols = len(maze[0])

def find_start(maze):
    for i in range(rows):
        for j in range(cols):
            if (maze[i][j] == 'S'):
                return (i, j)
    return None

def is_valid(x, y, visited):
    if (x < 0 or x >= rows or y < 0 or y >= cols):
        return False

    if (maze[x][y] == 1):
        return False

    if (x, y) in visited:
        return False
    return True

def depthlimitedsearch(position, depth, limit, visited, path):
    x, y = position
    visited.append(position)
    path.append(position)

    if (maze[x][y] == 'G'):
        return True

    if (depth == limit):
        path.pop()
        return False

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for move in moves:
        nx = x + move[0]
        ny = y + move[1]

        if is_valid(nx, ny, visited):
            if depthlimitedsearch((nx, ny), depth + 1, limit, visited, path):
                return True

    path.pop()
    return False

def iterativedeepeningsearch(start):
    for limit in range(rows * cols):
        visited = []
        path = []

        if depthlimitedsearch(start, 0, limit, visited, path):
            return path

    return None

startpos = find_start(maze)

print(" Depth Limited DepthFirstSearch with limit = 10 :")
visited = []
path = []
limit = 10

if depthlimitedsearch(startpos, 0, limit, visited, path):
    print("Path Found:", path)
else:
    print("No Path Found")

print(" Iterative Deepening Search = ")

ids_path = iterativedeepeningsearch(startpos)

if (ids_path):
    print("Path Found:", ids_path)
else:
    print("No Path Found")

# So Why Iterative Deepening Search is more suitable than Depth first search :
# 1.Depth-Limited DFS depends heavily on chosen limit.
#  If limit is too small then it will not find the goal probably.
#  If limit is  large then it will just behaves like normal DFS and may explore deep wrong paths first.
# 2.In unknown maze, goal depth is not known. DFS can go deep into dead ends before finding goal.
# 3.Iterative depeening search it combines advantages of BFS and DFS:
#  Like Depth first search it has a low memory usage.
#  In Best first search guarantees finding shallowest solution.
# 4. Iterative depeening search the depth increases normally in systematic way.
# So it will always find the goal at minimum depth.
# Therefore, for unknown goal depth and no heuristic guidance,
# Iterative Deepening Search is more suitable.
