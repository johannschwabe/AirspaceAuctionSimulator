import random

from Simulator import PathOwner
from ..Agents.PriorityPathAgent import PriorityPathAgent


class PriorityPathOwner(PathOwner):
    label = "Priority Path Owner"
    description = "Priority Path Owner"

    def __init__(self, owner_id, name, color, stops, creation_ticks, priority=random.random()):
        super().__init__(owner_id, name, color, stops, creation_ticks)
        self.priority = priority

    def initialize_agent(self, locations, stays, speed, battery, near_radius):
        agent_id: str = self.get_agent_id()
        return PriorityPathAgent(agent_id, locations, self.priority, stays, speed=speed, battery=battery,
                                 near_radius=near_radius)
