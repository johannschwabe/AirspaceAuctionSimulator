from typing import List, TYPE_CHECKING

from ..Agent.Agent import Agent
from ..Agent.PathAgent import PathAgent
from ..Enum import Reason

if TYPE_CHECKING:
    from ..Path import PathSegment


class PathReallocation:
    def __init__(self, agent: PathAgent, segments: List["PathSegment"], reason: Reason):
        self.agent = agent
        self.segments = segments
        self.reason = reason

    def correct_agent(self, agent: Agent):
        if isinstance(agent, PathAgent):
            return PathReallocation(agent, self.segments, self.reason)
        raise Exception("Invalid Agent Type")
