import heapq

def distance(x, y):
      return abs(x[0]-y[0]) + abs(x[1]-y[1])

robot = (0,0)

objects = [(2,1),(1,3),(4,2)]
visited = []
collected = []

while objects:
    p = []

    for obj in objects:
         d = distance(robot, obj)
         heapq.heappush(p, (d, obj))

    dist, nearest = heapq.heappop(p)

    print("Robot moves from", robot, "to", nearest)

    robot = nearest
    collected.append(nearest)
    objects.remove(nearest)

print("Collected objects are :", collected)
