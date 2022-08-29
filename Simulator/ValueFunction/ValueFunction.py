from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from Simulator.Agents.Agent import Agent

if TYPE_CHECKING:
    from Simulator.Segments.Segment import Segment


class ValueFunction(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def value_for_segments(self, segments: List["Segment"], agent: "Agent"):
        pass
