import random

class GoalBasedAgent:
    def __init__(self, environment):
        self.environment = environment
        self.position = 0
        self.goal = "Clean All Rooms"
        self.steps = 0

    def perceive(self):
        return self.environment[self.position]

    def act(self):
        percept = self.perceive()

        print("Step self.steps")
        print("Current Position:", self.position)
        print("Percept (Room Status):", percept)
        print("Goal:", self.goal)

        if percept == "Dirty":
            action = "Clean"
            self.environment[self.position] = "Clean"
        elif self.position < len(self.environment) - 1:
            action = "Move Right"
            self.position += 1
        else:
            action = "Stop"

        print("Action Taken:", action)
        self.steps += 1

    def run(self):
        while "Dirty" in self.environment:
            self.act()
        print("All rooms cleaned successfully!")
        print("Final Environment:", self.environment)

rooms = ["Dirty" if random.random() < 0.6 else "Clean" for _ in range(5)]

print("Initial Environment:", rooms)

agent = GoalBasedAgent(rooms)
agent.run()
