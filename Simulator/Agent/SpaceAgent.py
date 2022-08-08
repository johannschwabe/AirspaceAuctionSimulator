from abc import ABC

from .Agent import Agent
from .AllocationType import AllocationType
from ..Path import SpaceSegment


class SpaceAgent(Agent, ABC):
    allocation_type: str = AllocationType.SPACE.value

    def __init__(self):
        super().__init__()

    def add_allocated_segment(self, space_segment: SpaceSegment):
        self._allocated_segments.append(space_segment)
