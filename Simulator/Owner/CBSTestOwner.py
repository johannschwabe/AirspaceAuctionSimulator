from typing import List, TYPE_CHECKING

from ..Coordinate import TimeCoordinate
from .Owner import Owner
from ..Time import Tick
from ..Agent import ABAgent

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Agent import Agent


class CBSTestOwner(Owner):
    def __init__(self, name: str, color: str, creation_ticks: List[int]):
        super().__init__(name, color)
        self.creation_ticks = creation_ticks

    def generate_agents(self, t: int, env: "Environment") -> List["Agent"]:
        res = []
        if t == 0:
            start_1 = TimeCoordinate(0,5,0,Tick(0))
            end_1 = TimeCoordinate(5,0,0,Tick(7))
            start_2 = TimeCoordinate(5,0,0,Tick(0))
            end_2 = TimeCoordinate(0,5,0,Tick(7))

            res.append(ABAgent(start_1, end_1, 1, 20))
            res.append(ABAgent(start_2, end_2, 1, 20))
        self.agents += res
        return res
