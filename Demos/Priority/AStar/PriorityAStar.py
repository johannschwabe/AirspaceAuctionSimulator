from Demos.Priority.BidTracker.PriorityBidTracker import PriorityBidTracker
from Simulator import AStar


class PriorityAStar(AStar):
    def __init__(self,
                 environment,
                 bid_tracker: PriorityBidTracker,
                 tick,
                 max_iter=100_000,
                 g_sum=0.5,
                 height_adjust=0.05):
        super().__init__(environment, bid_tracker, tick, max_iter, g_sum, height_adjust)
        self.bid_tracker = bid_tracker

    def is_valid_for_allocation(self, position, agent):
        if self.environment.is_blocked(position, agent):
            return False, set()

        if position.t == self.tick:
            my_pos = agent.get_position_at_tick(self.tick)
            if my_pos is None:
                return False, set()
            elif my_pos == position:
                return True, set()
            raise Exception(f"JOHANN")

        agents = self.environment.intersect(position, agent.near_radius, agent.speed)
        colliding_agents = set()
        for agent_hash in agents:
            if agent_hash == agent.id:
                continue
            colliding_agent = self.environment.agents[agent_hash]
            if self.bid_tracker.get_last_bid_for_tick(
                self.tick, colliding_agent,
                self.environment).priority < self.bid_tracker.get_last_bid_for_tick(self.tick, colliding_agent,
                                                                                    self.environment).priority:
                colliding_agents.add(colliding_agent)
            else:
                return False, set()
        return True, colliding_agents
