from typing import Optional

from Bidding.BiddingABAgent import BiddingABAgent
from Bidding.BiddingNode import BiddingNode
from Simulator import Environment
from Simulator.AStar.AStar import AStar
from Simulator.Coordinate import Coordinate4D


class BiddingAStar(AStar):
    def __init__(self,
                 environment: "Environment",
                 max_iter: int = 100_000,
                 g_sum: float = 0.5,
                 height_adjust: Optional[str] = None):
        super().__init__(environment, max_iter, g_sum, height_adjust)
        self.node_class = BiddingNode

    def is_valid_for_allocation(self, position: "Coordinate4D", agent: "BiddingABAgent"):
        if self.environment.is_blocked(position, agent.near_radius, agent.speed):
            return False, set()
        agents = self.environment.intersect(position, agent.near_radius, agent.speed)
        res = set()
        for agent_id in agents:
            if agent_id == agent.id:
                continue
            colliding_agent = self.environment.get_agent(agent_id)
            if colliding_agent.priority < agent.priority:
                res.add(colliding_agent)
            else:
                return False, set()
        return True, res
