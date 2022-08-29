from Simulator import Bid


class PriorityPathBid(Bid):
    def __init__(self, agent, locations, stays, battery, priority, flying):
        super().__init__(agent)
        # locations this agent still wants to visit
        self.locations = locations
        # stay durations for the locations
        self.stays = stays
        # remaining battery (in ticks)
        self.battery = battery
        # priority in collisions
        self.priority = priority
        # if the agent is currently in the air
        self.flying = flying

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority
