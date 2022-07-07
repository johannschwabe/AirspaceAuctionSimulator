from typing import List

from ..Agent.SpaceAgent import SpaceAgent
from ..Agent.Agent import Agent
from ..Enum import Reason
from . import SpaceSegment


class SpaceReallocation:
    def __init__(self, agent: SpaceAgent, segments: List[SpaceSegment], reason: Reason,  compute_time: float = 0):
        self.agent = agent
        self.segments = segments
        self.reason = reason
        self.compute_time = compute_time

    def correct_agent(self, agent: Agent):
        if isinstance(agent, SpaceAgent):
            return SpaceReallocation(agent, self.segments, self.reason, self.compute_time)
        raise Exception("Invalid Agent Type")

