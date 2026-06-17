import heapq
from heapq import nsmallest

graph = {
'A': [('B', 2), ('C', 3), ('D', 1)],
'B': [('E', 3), ('F', 2)],
'C': [('G', 2), ('H', 4)],
'D': [('I', 6), ('J', 3)],
'E': [('K', 1), ('L', 2)],
'F': [('M', 4)],
'G': [('N', 1)],
'H': [('O', 3)],
'I': [('P', 2)],
'J': [('Q', 1)],
'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': []
}

start_node = 'A'
goal_node = 'N'


def dynamic_beam_search(graph, start, goal, initial_width, max_width):
  beam_width = initial_width
  level = 0
  beam = [(start, [start], 0)] # Each element: (current_node, path, total_cost)

  while beam:
      level += 1
      print(f"\nLevel {level} | Beam Width: {beam_width}")
      print("Current Beam :", [node for node, _, _ in beam])
      candidates = []
      for node, path, cost in beam:
          if node == goal:
              print("\nGoal Found!")
              print("Path:", path)
              print("Total Cost:", cost)
              return path, cost

          for neighbor, edge_cost in graph.get(node, []):
                        candidates.append((neighbor, path + [neighbor], cost + edge_cost))

      beam = nsmallest(initial_width,candidates,key=lambda x: x[0])

      if level % 3 == 0 and beam_width < max_width:
                beam_width += 1
                print(f"Beam width increased to {beam_width}")

  print("Goal not reachable.")
  return None, float('inf')

path, cost = dynamic_beam_search(graph, start_node, goal_node, 2,5)


