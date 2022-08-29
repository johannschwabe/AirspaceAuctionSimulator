from Simulator import Bid, PathAgent


class FCFSPathBid(Bid):
    def __init__(self, agent: "PathAgent"):
        super().__init__(agent)
