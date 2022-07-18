from typing import List, TYPE_CHECKING

from .Reason import Reason
from ..Agent.Agent import Agent
from ..Agent.PathAgent import PathAgent

if TYPE_CHECKING:
    from ..Path import PathSegment


class PathReallocation:
    def __init__(self, agent: PathAgent, segments: List["PathSegment"], reason: Reason, compute_time: float = 0):
        self.agent = agent
        self.segments = segments
        self.reason = reason
        self.compute_time = compute_time

    def correct_agent(self, agent: Agent):
        if isinstance(agent, PathAgent):
            return PathReallocation(agent, self.segments, self.reason, self.compute_time)
        raise Exception("Invalid Agent Type")
