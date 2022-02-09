import random

from Agent import Agent


class AgentA(Agent):
    def __init__(self):
        steps = random.randint(2, 5)
        for _ in range(steps):

        super().__init__(100, 0, 0,)
