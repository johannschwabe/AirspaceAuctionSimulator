from AAS import ABCAgent, Coordinate4D, Simulator
from Demos.FCFS.Bids.FCFSABCBid import FCFSABCBid


class FCFSABCAgent(ABCAgent):
    def __init__(
        self,
        locations: list[Coordinate4D],
        stays: list[int],
        simulator: Simulator,
        agent_id: int | None = None,
        speed: int | None = None,
        battery: int | None = None,
        near_radius: int | None = None,
    ):
        super().__init__(locations,
                         stays,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)

    def get_bid(self) -> FCFSABCBid:
        return FCFSABCBid(self.battery, self._locations, self.stays)

    def clone(self):
        clone = FCFSABCAgent(self.locations,
                             self.stays,
                             self.simulator,
                             agent_id=self.agent_id,
                             speed=self.speed,
                             battery=self.battery,
                             near_radius=self.near_radius)
        clone.allocated_segments = [segment.clone() for segment in self.allocated_segments]
        return clone
