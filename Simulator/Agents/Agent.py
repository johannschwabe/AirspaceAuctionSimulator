from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from ..Allocation.Segment import Segment
    from ..Simulator import Simulator
    from ..Bids.Bid import Bid


class Agent(ABC):
    agent_type: str
    allocation_type: str

    def __init__(self,
                 simulator: "Simulator",
                 agent_id: Optional[int] = None):

        self.simulator: "Simulator" = simulator

        if agent_id is not None:
            self.id: int = agent_id
            self.is_clone: bool = True
        else:
            self.id: int = self.simulator.get_agent_id()
            self.is_clone: bool = False

        self.allocated_segments: List["Segment"] = []

    @abstractmethod
    def value_for_segments(self, segments: List["Segment"]) -> float:
        pass

    @abstractmethod
    def get_bid(self, t: int) -> "Bid":
        pass

    @abstractmethod
    def initialize_clone(self) -> "Agent":
        pass

    def clone(self):
        clone = self.initialize_clone()
        clone.allocated_segments = [segment.clone() for segment in self.allocated_segments]
        return clone

    def get_allocated_value(self) -> float:
        return self.value_for_segments(self.allocated_segments)

    def __repr__(self):
        return f"{self.agent_type}-{self.id}"

    @abstractmethod
    def add_allocated_segment(self, path_segment: "Segment"):
        pass
