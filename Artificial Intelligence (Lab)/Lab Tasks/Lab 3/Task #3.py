import random

rooms = 5
actions = ["Clean", "Move"]
alpha = 0.1
gamma = 0.9
epsilon = 0.2
episodes = 100

Q = [[0 for x in range(len(actions))] for x in range(rooms)]

for episode in range(episodes):

    position = random.randint(0, rooms - 1)
    environment = []
    for i in range(rooms):
        if random.random() < 0.5:
            environment.append("Dirty")
        else:
            environment.append("Clean")

    for step in range(20):
        if random.random() < epsilon:
            action_index = random.randint(0, 1)
        else:
            action_index = Q[position].index(max(Q[position]))

        action = actions[action_index]

        if action == "Clean":
            if environment[position] == "Dirty":
                reward = 10
            else:
                reward = -1
            environment[position] = "Clean"
            next_position = position

        else:
            reward = -1
            if position < rooms - 1:
                next_position = position + 1
            else:
                next_position = position
        old_value = Q[position][action_index]
        next_max = max(Q[next_position])

        new_value = old_value + alpha * (reward + gamma * next_max - old_value)
        Q[position][action_index] = new_value

        position = next_position

print("Final Learned Q-Table:")
for i in range(rooms):
    print("Room", i, ":", Q[i])
