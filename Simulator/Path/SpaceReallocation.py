from typing import List

from ..Agent.SpaceAgent import SpaceAgent
from ..Agent.Agent import Agent
from ..Enum import Reason
from . import SpaceSegment


class SpaceReallocation:
    def __init__(self, agent: SpaceAgent, segments: List[SpaceSegment], reason: Reason):
        self.agent = agent
        self.segments = segments
        self.reason = reason

    def correct_agent(self, agent: Agent):
        if isinstance(agent, SpaceAgent):
            return SpaceReallocation(agent, self.segments, self.reason)
        raise Exception("Invalid Agent Type")

