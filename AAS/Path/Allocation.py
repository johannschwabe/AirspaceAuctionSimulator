from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agent.Agent import Agent
    from .AllocationReason import AllocationReason


class Allocation(ABC):
    def __init__(self, agent: "Agents", reason: "AllocationReason", compute_time: float = 0):
        self.agent = agent
        self.reason = reason
        self.compute_time = compute_time

    @abstractmethod
    def correct_agent(self, agent: "Agents"):
        pass
