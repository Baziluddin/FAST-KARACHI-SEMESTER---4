import random

class SimpleReflexAgent:
    def __init__(self, environment):
        self.env = environment.copy()
        self.position = 0
        self.steps = 0

    def run(self):
        while "Dirty" in self.env:
            if self.env[self.position] == "Dirty":
                self.env[self.position] = "Clean"
            elif self.position < len(self.env) - 1:
                self.position += 1
            self.steps += 1
        return self.steps


class LearningAgent:
    def __init__(self, environment):
        self.env = environment.copy()
        self.position = 0
        self.steps = 0

    def run(self):
        while "Dirty" in self.env:
            if self.env[self.position] == "Dirty":
                self.env[self.position] = "Clean"
            else:
                self.position = random.randint(0, len(self.env) - 1)
            self.steps += 1
        return self.steps

rooms = ["Dirty" if random.random() < 0.6 else "Clean" for x in range(5)]
print("Initial Environment:", rooms)
reflex_agent = SimpleReflexAgent(rooms)
learning_agent = LearningAgent(rooms)
reflex_steps = reflex_agent.run()
learning_steps = learning_agent.run()
print("Simple Reflex Agent Steps:", reflex_steps)
print("Learning Agent Steps:", learning_steps)
if learning_steps < reflex_steps:
    print("Learning Agent performed better.")
else:
    print("Simple Reflex Agent performed better.")
