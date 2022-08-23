from Simulator import PathBid


class FCFSPathBid(PathBid):
    def __init__(self, battery, locations, stays):
        super().__init__(battery, locations, stays)
