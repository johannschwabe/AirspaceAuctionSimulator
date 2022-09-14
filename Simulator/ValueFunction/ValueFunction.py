from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

from Simulator.Agents.Agent import Agent

if TYPE_CHECKING:
    from Simulator.Segments.Segment import Segment


class ValueFunction(ABC):
    label: str = "Abstract Value Function"
    description: str = "The description for a concrete value function"

    @abstractmethod
    def value_for_segments(self, segments: List["Segment"], agent: "Agent"):
        pass
