from abc import ABC

from Coords import Coords


class Agent(ABC):
    id = 0

    def __init__(self, start: Coords, target: Coords):
        self.start = start
        self.target = target
        self.id = Agent.id
        Agent.id += 1
