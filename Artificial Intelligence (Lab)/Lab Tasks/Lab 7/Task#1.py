colors = ["Red", "Green", "Blue"]

graph = {
    'A': ['B', 'E'],
    'B': ['A', 'C', 'D'],
    'C': ['B', 'D'],
    'D': ['B', 'C', 'E'],
    'E': ['A', 'D']
}

def validCheck(node, color, assignment):
    for neighbor in graph[node]:
        if (neighbor in assignment and assignment[neighbor] == color):
            return False
    return True


def backtrack(assignment):
    if (len(assignment) == len(graph)):
        print(assignment)
        return

    node = [n for n in graph if n not in assignment][0]

    for color in colors:
        if (validCheck(node, color, assignment)):
            assignment[node] = color
            backtrack(assignment)
            del assignment[node]

backtrack({})
