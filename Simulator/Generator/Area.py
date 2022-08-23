from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from API import APISimpleCoordinates


class LongLatCoordinate:
    """
    Wrapper for long-lat coordinates
    """
    def __init__(self, long, lat):
        self.long = long
        self.lat = lat


class Area:
    """
    Wrapper for field bounds defined by the bottom-left coordinate (in long-lat) and top-right coordinate (in long-lat)
    and the grid size in meters
    """
    def __init__(self, bottom_left_ll: "APISimpleCoordinates", top_right_ll: "APISimpleCoordinates", resolution: int):
        self.bottom_left = LongLatCoordinate(bottom_left_ll.long, bottom_left_ll.lat)
        self.top_right = LongLatCoordinate(top_right_ll.long, top_right_ll.lat)
        self.resolution = resolution
