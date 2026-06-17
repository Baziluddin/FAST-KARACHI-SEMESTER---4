import math

class Node:
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children or []
        self.minmax_value = None

class Minimax:
    def __init__(self):
        self.computed_nodes = []

    def compute_minimax(self, node, depth, maximizing_player=True):
        if (depth == 0 or not node.children):
            self.computed_nodes.append(node.value)
            return node.value

        if (maximizing_player):
            value = -math.inf
            for child in node.children:
                child_value = self.compute_minimax(child, depth - 1, False)
                value = max(value, child_value)
            node.minmax_value = value
            self.computed_nodes.append(value)
            return value
        else:
            value = math.inf
            for child in node.children:
                child_value = self.compute_minimax(child, depth - 1, True)
                value = min(value, child_value)
            node.minmax_value = value
            self.computed_nodes.append(value)
            return value


D = Node(children=[Node(3), Node(5)])
E = Node(children=[Node(6), Node(9)])
F = Node(children=[Node(1), Node(2)])
G = Node(children=[Node(0), Node(-1)])

B = Node(children=[D, E])
C = Node(children=[F, G])

A = Node(children=[B, C])

solver = Minimax()
result = solver.compute_minimax(A, 3, True)

print("D : ", D.minmax_value)
print("E : ", E.minmax_value)
print("F : ", F.minmax_value)
print("G : ", G.minmax_value)
print("B : ", B.minmax_value)
print("C : ", C.minmax_value)
print("A ; ", result)

best_move = "B" if B.minmax_value >= C.minmax_value else "C"
print(" Best move for Max:", best_move)
