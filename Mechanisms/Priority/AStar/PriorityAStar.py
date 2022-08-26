from Simulator import AStar


class PriorityAStar(AStar):
    def __init__(self,
                 environment,
                 tick,
                 max_iter=100_000,
                 g_sum=0.5,
                 height_adjust=0.05):
        super().__init__(environment, tick, max_iter, g_sum, height_adjust)

    def is_valid_for_allocation(self, position, agent):
        if self.environment.is_blocked(position, agent):
            return False, set()
        agents = self.environment.intersect(position, agent.near_radius, agent.speed)
        colliding_agents = set()
        for agent_hash in agents:
            if agent_hash == agent.id:
                continue
            colliding_agent = self.environment.agents[agent_hash]
            if colliding_agent.get_bid(self.tick, self.environment).priority < agent.get_bid(self.tick,
                                                                                             self.environment).priority:
                colliding_agents.add(colliding_agent)
            else:
                return False, set()
        return True, colliding_agents
