from Simulator import Bid
from Simulator.Agents.SpaceAgent import SpaceAgent


class PrioritySpaceBid(Bid):
    def __init__(self, agent: "SpaceAgent", priority):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "SpaceAgent" = agent
        # priority in collisions
        self.priority = priority
