from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from .AllocationReason import AllocationReason
    from .Segment import Segment


class Allocation(ABC):
    def __init__(self,
                 agent: "Agent",
                 segments: List["Segment"],
                 reason: "AllocationReason",
                 compute_time: int = 0):
        self.agent: "Agent" = agent
        self.reason: "AllocationReason" = reason
        self.compute_time: int = compute_time
        self.segments: List["Segment"] = segments

    @abstractmethod
    def correct_agent(self, agent: "Agent"):
        pass
