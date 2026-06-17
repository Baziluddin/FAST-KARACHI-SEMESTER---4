import heapq

graph = {
    "Arad": {"Zerind":75, "Timisoara":118, "Sibiu":140},
    "Zerind": {"Arad":75, "Oradea":71},
    "Oradea": {"Zerind":71, "Sibiu":151},
    "Timisoara": {"Arad":118, "Lugoj":111},
    "Lugoj": {"Timisoara":111, "Mehadia":70},
    "Mehadia": {"Lugoj":70, "Drobeta":75},
    "Drobeta": {"Mehadia":75, "Craiova":120},
    "Craiova": {"Drobeta":120, "Pitesti":138, "Rimnicu Vilcea":146},
    "Sibiu": {"Arad":140, "Fagaras":99, "Rimnicu Vilcea":80},
    "Fagaras": {"Sibiu":99, "Bucharest":211},
    "Rimnicu Vilcea": {"Sibiu":80, "Pitesti":97, "Craiova":146},
    "Pitesti": {"Rimnicu Vilcea":97, "Craiova":138, "Bucharest":101},
    "Bucharest": {"Fagaras":211, "Pitesti":101}
}

def Uniformcostsearch_graph(start, goal):
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)
        path = path + [node]

        if node == goal:
            return path, cost

        for neighbor in graph[node]:
            heapq.heappush(pq, (cost + graph[node][neighbor], neighbor, path))

    return None

print("Output is :")
print(Uniformcostsearch_graph("Arad","Bucharest"))
