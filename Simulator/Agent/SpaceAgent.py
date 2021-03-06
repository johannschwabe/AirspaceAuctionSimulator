from abc import ABC

from . import Agent
from ..Path import SpaceSegment


class SpaceAgent(Agent, ABC):
    def __init__(self):
        super().__init__()

    def add_allocated_segment(self, space_segment: SpaceSegment):
        self._allocated_segments.append(space_segment)

