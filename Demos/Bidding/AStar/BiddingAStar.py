from typing import Optional, Tuple, TYPE_CHECKING

from AAS.AStar.AStar import AStar
from Demos.Bidding.AStar.BiddingNode import BiddingNode

if TYPE_CHECKING:
    from AAS import Environment
    from AAS.Coordinates import Coordinate4D
    from Demos.Bidding.Agents.BiddingABAgent import BiddingABAgent


class BiddingAStar(AStar):
    def __init__(self,
                 environment: "Environment",
                 max_iter: int = 100_000,
                 g_sum: float = 0.5,
                 height_adjust: Optional[bool] = None):
        super().__init__(environment, max_iter, g_sum, height_adjust)
        self.node_class = BiddingNode

    def is_valid_for_allocation(self, position: "Coordinate4D", agent: "BiddingABAgent") -> Tuple[bool, set["Agents"]]:
        if self.environment.is_blocked(position, agent.near_radius, agent.speed):
            return False, set()
        agents = self.environment.intersect(position, agent.near_radius, agent.speed)
        colliding_agents: set["Agents"] = set()
        for agent_id in agents:
            if agent_id == agent.id:
                continue
            colliding_agent = self.environment.get_agent(agent_id)
            if colliding_agent.priority < agent.priority:
                colliding_agents.add(colliding_agent)
            else:
                return False, set()
        return True, colliding_agents
