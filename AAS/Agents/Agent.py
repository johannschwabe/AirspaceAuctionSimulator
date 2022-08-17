from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..Path import PathSegment, SpaceSegment
    from ..Simulator import Simulator
    from ..Bids import Bid
    from ..Coordinates import Coordinate4D


class Agent(ABC):
    agent_type: str
    allocation_type: str

    def __init__(
        self,
        simulator: "Simulator",
        agent_id: Optional[int] = None
    ):
        self.simulator: "Simulator" = simulator

        if agent_id is not None:
            self.id: int = agent_id
            self.is_clone: bool = True
        else:
            self.id: int = self.simulator.getAgentId()
            self.is_clone: bool = False

        self.allocated_segments: list["PathSegment" | "SpaceSegment"] = []
        self.optimal_welfare: float = 1.
        self.costs: float = 0.

    @property
    def achieved_welfare(self) -> float:
        return self.value_for_segments(self.allocated_segments)

    @abstractmethod
    def value_for_segments(self, segments: list["PathSegment" | "SpaceSegment"]) -> float:
        pass

    @abstractmethod
    def get_bid(self, t: int) -> "Bid":
        pass

    @abstractmethod
    def clone(self):
        pass

    def get_allocated_coords(self) -> list["Coordinate4D"]:
        return [coord for path_segment in self.allocated_segments for coord in path_segment.coordinates]

    def get_allocated_value(self) -> float:
        return self.value_for_segments(self.allocated_segments)

    def generalized_bid(self):
        return {
            "No Bids": "-",
            "!value": -1
        }

    def __repr__(self):
        return str(self.id)
