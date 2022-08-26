from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from Simulator.Agents.Agent import Agent
    from Simulator.Allocations.Allocation import Allocation
    from Simulator.Environment.Environment import Environment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate(self,
                 agents: List["Agent"],
                 env: "Environment",
                 tick: int) -> List["Allocation"]:
        pass

    @staticmethod
    def compatible_owner():
        pass
