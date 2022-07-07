from abc import ABC

from .Agent import Agent
from .AllocationType import AllocationType
from ..Path import SpaceSegment


class SpaceAgent(Agent, ABC):
    def __init__(self, agent_type: str):
        super().__init__(agent_type, AllocationType.SPACE.value)

    def add_allocated_segment(self, space_segment: SpaceSegment):
        self._allocated_segments.append(space_segment)

