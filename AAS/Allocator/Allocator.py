from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Path.Allocation import Allocation
    from ..Agents.Agent import Agent
    from ..Environment.Environment import Environment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agents(self,
                            agents: list["Agent"],
                            env: "Environment",
                            tick: int) -> list["Allocation"]:
        pass

    def temp_allocation(self,
                        agents: list["Agent"],
                        env: "Environment",
                        tick: int) -> list["Allocation"]:
        cloned_agents = [agent.clone() for agent in agents]
        return self.allocate_for_agents(cloned_agents, env, tick)

    @staticmethod
    def compatible_owner():
        pass
