import random
from collections import (deque)
import heapq

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_tree():
    alphabets = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(alphabets)

    nodes = [Node(ch) for ch in alphabets]

    for i in range(len(nodes)):
        left_index = 2*i + 1
        right_index = 2*i + 2

        if (left_index < len(nodes)):
            nodes[i].left = nodes[left_index]
        if (right_index < len(nodes)):
            nodes[i].right = nodes[right_index]

    return nodes[0]

def bfs(root, goal):
    queue = deque([root])

    while queue:
        node = queue.popleft()
        print(node.value, " ")

        if (node.value == goal):
            return "Found!"
        if (node.left):
            queue.append(node.left)
        if (node.right):
            queue.append(node.right)
    return "Not Found"

def dfs(root, goal):
    stack = [root]

    while stack:
        node = stack.pop()
        print(node.value, " ")

        if (node.value == goal):
            return "Found!"
        if (node.right):
            stack.append(node.right)
        if (node.left):
            stack.append(node.left)
    return "Not Found"

def dls(node, goal, depth):
    if (node is None):
        return False

    print(node.value, " ")

    if (node.value == goal):
        return True

    if (depth <= 0):
        return False

    return (dls(node.left, goal, depth-1) or
            dls(node.right, goal, depth-1))

def Iterativedeepeningsearch(root, goal, maxdepth):

    for depth in range(maxdepth):
        print(" Depth:", depth)
        if (dls(root, goal, depth)):
            return " Succesfully Found! "
    return " Not Found "

def UniformCostSearch(root, goal):

    pq = []
    countotal=0
    heapq.heappush(pq, (0,countotal, root))

    while pq:
        cost,_, node = heapq.heappop(pq)
        print(node.value, " ")

        if (node.value == goal):
            return "Found with the cost =  " + str(cost)
        if (node.left):
            countotal = countotal +1
            heapq.heappush(pq, (cost+1,countotal, node.left))
        if (node.right):
            countotal = countotal + 1
            heapq.heappush(pq, (cost+1,countotal, node.right))

    return "Not Found"

root = build_tree()
goal = 'G'
print(" BFS :")
print(bfs(root, goal))

print(" DFS :")
print(dfs(root, goal))

print(" IDS : ")
print(Iterativedeepeningsearch(root, goal, 5))

print(" Uniform cost =")
print(UniformCostSearch(root,goal))
