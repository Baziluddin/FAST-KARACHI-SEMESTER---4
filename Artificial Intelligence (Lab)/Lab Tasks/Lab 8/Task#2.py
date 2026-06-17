import math

class Node:
    def __init__(self, value=None, children=None, name=""):
        self.value = value
        self.children = children or []
        self.name = name

class AlphaBeta:
    def __init__(self):
        self.visited = 0
        self.pruned = []

    def compute(self, node, depth, alpha, beta, maximizing):
        if (depth == 0 or not node.children):
            self.visited += 1
            return node.value

        if (maximizing):
            value = -math.inf
            for child in node.children:
                val = self.compute(child, depth - 1, alpha, beta, False)
                value = max(value, val)
                alpha = max(alpha, value)
                if (beta <= alpha):
                    self.pruned.append(child.name)
                    break
            return value
        else:
            value = math.inf
            for child in node.children:
                val = self.compute(child, depth - 1, alpha, beta, True)
                value = min(value, val)
                beta = min(beta, value)
                if (beta <= alpha):
                    self.pruned.append(child.name)
                    break
            return value


D = Node(children=[Node(3), Node(5)], name="D")
E = Node(children=[Node(6), Node(9)], name="E")
F = Node(children=[Node(1), Node(2)], name="F")
G = Node(children=[Node(0), Node(-1)], name="G")

B = Node(children=[D, E], name="B")
C = Node(children=[F, G], name="C")

A = Node(children=[B, C], name="A")

solver = AlphaBeta()
result = solver.compute(A, 3, -math.inf, math.inf, True)

print(" Optmal value at A:", result)
print(" Nodes Evaluated using Alpha-Beta algo is :", solver.visited)
print(" The Pruned branches are :", solver.pruned)

minimax_nodes = 8
print(" N odes Evaluated Minimax ", minimax_nodes)
print(" efficiency gain :", minimax_nodes - solver.visited)
