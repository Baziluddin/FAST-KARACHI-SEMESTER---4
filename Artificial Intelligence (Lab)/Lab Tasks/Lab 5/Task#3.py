import heapq

graph = {
'A': [('B',2), ('C',4)],
'B': [('D',3)],
'C': [('D',1)],
'D': [('E',2)],
'E': []
}

heuristic = {
'A':7,
'B':4,
'C':2,
'D':1,
'E':0
}

start = 'A'
goal = 'E'

open_list = []
heapq.heappush(open_list,(0,start))

g = {start:0}
closed = []

while open_list:

   f,current = heapq.heappop(open_list)

   print("Visiting:",current)

   if (current == goal):
        print(" Evacuation point reached. ")
        break

   closed.append(current)

   for neighbor,cost in graph[current]:
       if (neighbor in closed):
         continue

       new_g = g[current] + cost
       g[neighbor] = new_g
       f = new_g + heuristic[neighbor]
       heapq.heappush(open_list,(f,neighbor))
