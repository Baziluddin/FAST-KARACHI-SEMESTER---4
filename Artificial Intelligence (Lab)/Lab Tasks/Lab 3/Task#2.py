import random

class UtilityBasedAgent:
    def __init__(self, environment):
        self.environment = environment
        self.position = 0
        self.total_utility = 0

    def perceive(self):
        return self.environment[self.position]

    def calculate_utilities(self):
        utilities = {}

        if self.environment[self.position] == "Dirty":
            utilities["Clean"] = 10
        else:
            utilities["Clean"] = -1

        if self.position < len(self.environment) - 1:
            utilities["Move"] = 2
        else:
            utilities["Move"] = -5

        utilities["Do Nothing"] = 0

        return utilities

    def act(self):
        utilities = self.calculate_utilities()
        best_action = max(utilities, key=utilities.get)
        best_value = utilities[best_action]

        print("Current Position:", self.position)
        print("Room Status:", self.environment[self.position])
        print("Selected Action:", best_action)
        print("Utility Value:", best_value)

        if best_action == "Clean":
            self.environment[self.position] = "Clean"
        elif best_action == "Move":
            self.position += 1

        self.total_utility += best_value
        print("Total Utility So Far:", self.total_utility)

    def run(self):
        for _ in range(len(self.environment) * 2):
            self.act()

        print("Final Utility:", self.total_utility)
        print("Final Environment:", self.environment)


rooms = ["Dirty" if random.random() < 0.5 else "Clean" for x in range(5)]
print("Initial Environment:", rooms)

agent = UtilityBasedAgent(rooms)
agent.run()
