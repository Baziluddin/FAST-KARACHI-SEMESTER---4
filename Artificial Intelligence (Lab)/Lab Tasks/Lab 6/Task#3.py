import random

teachers = ['T1','T2','T3','T4','T5']
courses = ['C1','C2','C3','C4','C5']
days = 5
slots_per_day = 5
total_slots = days * slots_per_day

POP_SIZE = 20
GENERATIONS = 200
MUTATION_RATE = 0.1


def initialize_population():
    population = []
    for _ in range(POP_SIZE):
         chromosome = []
         for _ in range(total_slots):
               teacher = random.choice(teachers)
               course = random.choice(courses)
               chromosome.append((teacher, course))
         population.append(chromosome)

    return population


def fitness(chromosome):
    penalty = 0
    for slot_index in range(slots_per_day):
          slot_teachers = []
          for day in range(days):
              teacher, _ = chromosome[day*slots_per_day + slot_index]
              if teacher in slot_teachers:
                  penalty += 1
              else:
                   slot_teachers.append(teacher)


    course_count = {c:0 for c in courses}
    for _, course in chromosome:
         course_count[course] += 1
    for count in course_count.values():
          penalty += abs(3 - count)


    for day in range(days):
      for teacher in teachers:
         consecutive = 0
         for slot in range(slots_per_day):
            idx = day*slots_per_day + slot
            if chromosome[idx][0] == teacher:
                 consecutive += 1
                 if consecutive > 3:
                      penalty += 1
                 else:
                      consecutive = 0


      return 1 / (1 + penalty)


def select_parents(population):
    fitness_values = [fitness(c) for c in population]
    total = sum(fitness_values)
    probs = [f/total for f in fitness_values]
    parents = random.choices(population, weights=probs, k=2)
    return parents


def crossover(parent1, parent2):
    point = random.randint(1, total_slots-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(chromosome):
    for i in range(total_slots):
        if random.random() < MUTATION_RATE:
            teacher = random.choice(teachers)
            course = random.choice(courses)
            chromosome[i] = (teacher, course)
    return chromosome


def genetic_algorithm():
  population = initialize_population()
  best_chromosome = None
  best_fitness = 0

  for gen in range(GENERATIONS):
      new_population = []

      while len(new_population) < POP_SIZE:
           parent1, parent2 = select_parents(population)
           child1, child2 = crossover(parent1, parent2)
           child1 = mutate(child1)
           child2 = mutate(child2)
           new_population.extend([child1, child2])

           population = new_population[:POP_SIZE]
           current_best = max(population, key=fitness)
           current_fit = fitness(current_best)
           if current_fit > best_fitness:
                  best_fitness = current_fit
                  best_chromosome = current_best

           if gen % 20 == 0:
                print("Generation ",gen," Best Fitness = ",best_fitness)

                print("Best Timetabe Fitness:", best_fitness)
                print("Best Timetabe (Teacher, Course).")

      return best_chromosome


genetic_algorithm()
