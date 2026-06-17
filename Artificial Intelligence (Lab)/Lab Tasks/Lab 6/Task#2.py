import random


def calculate_conflicts(state):
  conflicts = 0
  n = len(state)
  for i in range(n):
    for j in range(i + 1, n):
         if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
             conflicts += 1
  return conflicts


def get_neighbors(state):

  neighbors = []
  n = len(state)
  for col in range(n):
     for row in range(n):
         if row != state[col]:
              new_state = list(state)
              new_state[col] = row
              neighbors.append(new_state)

  return neighbors


def hill_climbing(n, initial_state):

  current_state = initial_state
  current_conflicts = calculate_conflicts(current_state)

  while True:
     neighbors = get_neighbors(current_state)
     next_state = None
     next_conflicts = current_conflicts

     for neighbor in neighbors:
          neighbor_conflicts = calculate_conflicts(neighbor)
          if neighbor_conflicts < next_conflicts:
               next_state = neighbor
               next_conflicts = neighbor_conflicts
               break


     if next_conflicts >= current_conflicts:
        break

     current_state = next_state
     current_conflicts = next_conflicts

     return current_state, current_conflicts


def random_restart_hill_climbing(n, max_restarts=20):

    restart_count = 0
    best_state = None
    best_conflicts = n * (n - 1) // 2

    while restart_count < max_restarts:

         initial_state = [random.randint(0, n - 1) for _ in range(n)]
         solution, conflicts = hill_climbing(n, initial_state)


         if conflicts < best_conflicts:
                best_conflicts = conflicts
                best_state = solution

         if conflicts == 0:
                print(f"Solution found after {restart_count+1} restart(s)")
                return solution

         restart_count += 1

         print(f"No perfect solution found after {max_restarts} restarts")
         return best_state

N=10
solution = random_restart_hill_climbing(N)

print("Final State:", solution)
print("Conflicts:", calculate_conflicts(solution))
