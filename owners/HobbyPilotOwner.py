from typing import List

from Simulator import Owner, Environment, Agent
from Simulator.Coordinate import Coordinate
from agents.HobbyPilotAgent import HobbyPilotAgent


class HobbyPilotOwner(Owner):
    def __init__(self, corner1: Coordinate, corner2: Coordinate, t_start: int, t_stop: int, t_init: int):
        super().__init__()

        assert corner1 <= corner2
        assert t_start <= t_stop
        assert t_init >= 0

        self.corner1 = corner1
        self.corner2 = corner2
        self.t_start = t_start
        self.t_stop = t_stop
        self.t_init = t_init

    def generate_agents(self, t: int, env: Environment) -> List[Agent]:
        res = []
        if t == self.t_init:
            agent = HobbyPilotAgent(self.corner1, self.corner2, self.t_start, self.t_stop)
            res.append(agent)
            print(f"Hobby pilot created {agent}")

        self.agents += res
        return res
