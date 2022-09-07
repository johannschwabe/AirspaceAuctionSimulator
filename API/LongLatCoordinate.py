class LongLatCoordinate:
    """
    Wrapper for long-lat coordinates
    """

    def __init__(self, long: float, lat: float):
        self.long = long
        self.lat = lat

    def __repr__(self):
        return f"Coord<long={self.long}, lat={self.lat}>"

    def as_dict(self):
        return {
            "long": self.long,
            "lat": self.lat,
        }
