from AAS import ABAAgent, Coordinate4D, Simulator
from Demos.FCFS.Bids.FCFSABABid import FCFSABABid


class FCFSABAAgent(ABAAgent):

    def __init__(
        self,
        a: Coordinate4D,
        b: Coordinate4D,
        simulator: Simulator,
        agent_id: int | None = None,
        stay: int = 5,
        speed: int | None = None,
        battery: int | None = None,
        near_radius: int | None = None,
    ):
        super().__init__(a,
                         b,
                         simulator,
                         agent_id=agent_id,
                         stay=stay,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)

    def get_bid(self) -> FCFSABABid:
        return FCFSABABid(self.battery, self.a, self.b, self.stay)

    def clone(self):
        clone = FCFSABAAgent(self.a,
                             self.b,
                             self.simulator,
                             agent_id=self.id,
                             stay=self.stay,
                             speed=self.speed,
                             battery=self.battery,
                             near_radius=self.near_radius)
        clone.allocated_segments = [segment.clone() for segment in self.allocated_segments]
        return clone
