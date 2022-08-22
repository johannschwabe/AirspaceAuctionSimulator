from typing import Optional, Tuple, TYPE_CHECKING

from Demos.Priority.AStar.PriorityNode import PriorityNode
from Simulator.AStar.AStar import AStar

if TYPE_CHECKING:
    from Simulator import Environment
    from Simulator.Coordinates import Coordinate4D
    from Demos.Priority.Agents.PriorityABAgent import PriorityABAgent


class PriorityAStar(AStar):
    def __init__(self,
                 environment: "Environment",
                 max_iter: int = 100_000,
                 g_sum: float = 0.5,
                 height_adjust: Optional[bool] = None):
        super().__init__(environment, max_iter, g_sum, height_adjust)
        self.node_class = PriorityNode

    def is_valid_for_allocation(self, position: "Coordinate4D", agent: "PriorityABAgent") -> Tuple[bool, set["Agents"]]:
        if self.environment.is_blocked(position, agent.near_radius, agent.speed):
            return False, set()
        agents = self.environment.intersect(position, agent.near_radius, agent.speed)
        colliding_agents: set["Agents"] = set()
        for agent_id in agents:
            if agent_id == agent.id:
                continue
            colliding_agent = self.environment.agents[agent_id]
            if colliding_agent.priority < agent.priority:
                colliding_agents.add(colliding_agent)
            else:
                return False, set()
        return True, colliding_agents
