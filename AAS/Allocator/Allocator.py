from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Path.Allocation import Allocation
    from ..Agents.Agent import Agent
    from ..Environment.Environment import Environment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agents(self,
                            agents: List["Agent"],
                            env: "Environment",
                            tick: int) -> List["Allocation"]:
        pass

    def allocate(self,
                 agents: List["Agent"],
                 env: "Environment",
                 tick: int) -> List["Allocation"]:
        cloned_agents = [agent.clone() for agent in agents]
        return self.allocate_for_agents(cloned_agents, env, tick)

    @staticmethod
    def compatible_owner():
        pass
