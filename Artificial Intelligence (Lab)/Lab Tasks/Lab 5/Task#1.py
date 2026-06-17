import heapq

graph = {
'Gate': ['Library', 'Cafeteria'],
'Library': ['Lab', 'Admin'],
'Cafeteria': ['Admin'],
'Lab': ['Hostel'],
'Admin': ['Hostel'],
'Hostel': []
}

heuristic = {
'Gate': 10,
'Library': 6,
'Cafeteria': 7,
'Lab': 4,
'Admin': 3,
'Hostel': 0
}

start = 'Gate'
goal = 'Hostel'
Open_List = []
Closed_List = []
heapq.heappush(Open_List,(heuristic[start],start))

while Open_List:
     h,current = heapq.heappop(Open_List)
     print("Current node:",current)

     if (current == goal):
          print("Goal reached")
          break

     Closed_List.append(current)

     for neighbor in graph[current]:
            if (neighbor not in Closed_List):
                  heapq.heappush(Open_List,(heuristic[neighbor],neighbor))
