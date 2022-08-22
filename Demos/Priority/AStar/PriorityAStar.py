from Simulator.AStar.AStar import AStar


class PriorityAStar(AStar):
    def __init__(self,
                 environment,
                 max_iter=100_000,
                 g_sum=0.5,
                 height_adjust=None):
        super().__init__(environment, max_iter, g_sum, height_adjust)

    def is_valid_for_allocation(self, position, agent):
        if self.environment.is_blocked(position, agent):
            return False, set()
        agents = self.environment.intersect(position, agent.near_radius, agent.speed)
        colliding_agents = set()
        for agent_id in agents:
            if agent_id == agent.id:
                continue
            colliding_agent = self.environment.agents[agent_id]
            if colliding_agent.priority < agent.priority:
                colliding_agents.add(colliding_agent)
            else:
                return False, set()
        return True, colliding_agents
