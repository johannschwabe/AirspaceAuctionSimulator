from Simulator import PathAgent
from ..Bids.PriorityPathBid import PriorityPathBid


class PriorityPathAgent(PathAgent):
    def __init__(self,
                 agent_id,
                 locations,
                 priority,
                 stays,
                 speed=None,
                 battery=None,
                 near_radius=None,
                 _is_clone=False):
        super().__init__(agent_id,
                         locations,
                         stays,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius,
                         _is_clone=_is_clone)
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
        clone = PriorityPathAgent(self.id,
                                  self.locations,
                                  self.priority,
                                  self.stays,
                                  speed=self.speed,
                                  battery=self.battery,
                                  near_radius=self.near_radius,
                                  _is_clone=True)
        return clone
