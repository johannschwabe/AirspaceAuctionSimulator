from Demos.Priority.Bids.PriorityPathBid import PriorityPathBid
from Simulator import PathAgent


class PriorityPathAgent(PathAgent):
    def __init__(self,
                 locations,
                 priority,
                 simulator,
                 stays,
                 agent_id=None,
                 speed=None,
                 battery=None,
                 near_radius=None):
        super().__init__(locations,
                         stays,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)
        self.priority = priority

    def get_bid(self, t):
        flying = False
        locations = self.locations
        battery = self.battery
        stays = self.stays
        start = None
        if len(self.allocated_segments) > 0 and self.allocated_segments[0].min.t <= t:
            index = 0
            for i, segment in enumerate(self.allocated_segments):
                if segment.max.t >= t:
                    index = i
                    if segment.min.t < t:
                        flying = True
                        for coordinate in segment.coordinates:
                            if coordinate.t == t:
                                start = coordinate.clone()
                    else:
                        start = self.allocated_segments[i - 1].max.clone()
                        start.t += self.stays[i - 1]
                    break
            if start is None:
                raise Exception(f"Invalid segments allocated at tick {t}: {self.allocated_segments}")

            locations = self.locations[index + 1:]
            locations.insert(0, start)

            stays = self.stays[index:] if index < len(self.stays) else []

        return PriorityPathBid(battery, locations, stays, self.priority, flying)

    def initialize_clone(self):
        clone = PriorityPathAgent(self.locations,
                                  self.priority,
                                  self.simulator,
                                  self.stays,
                                  agent_id=self.id,
                                  speed=self.speed,
                                  battery=self.battery,
                                  near_radius=self.near_radius)
        return clone
