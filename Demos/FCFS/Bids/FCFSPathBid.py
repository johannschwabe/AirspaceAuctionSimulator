from Simulator import Bid, PathAgent


class FCFSPathBid(Bid):
    def __init__(self, agent: "PathAgent"):
        super().__init__(agent)

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return True
