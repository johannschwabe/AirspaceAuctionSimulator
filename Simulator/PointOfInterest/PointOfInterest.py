from ..Time import Tick
from ..Path import TravelPath
from ..Value import ValueFunction
from ..Value.SpatialValueFunction import SpatialOnlyOneValue
from ..Value.TemporalValueFunction import TemporalOnlyOneValue
from ..Coordinate import Coordinate, TimeCoordinate


class PointOfInterest:

    def __init__(self, location: Coordinate, tick: Tick):
        self.location = location
        self.tick = tick

        self._spatial_value_function: ValueFunction = SpatialOnlyOneValue(self.location)
        self._temporal_value_function: ValueFunction = TemporalOnlyOneValue(self.tick)

    def __repr__(self):
        return f"<{self.location}, {self.tick}>"

    def __str__(self):
        return f"<{self.location}, {self.tick}>"

    def value_of_path(self, path: TravelPath):
        max_value = -1
        for time_cord in path.locations:
            spatial_value = self._spatial_value_function(time_cord)
            temporal_value = self._temporal_value_function(time_cord.t)
            total_value = spatial_value * temporal_value
            max_value = max(max_value, total_value)
        return max_value

    def set_spatial_value_function(self, value_function: ValueFunction, **kwargs):
        self._spatial_value_function = value_function(self.location, **kwargs)

    def set_temporal_value_function(self, value_function: ValueFunction, **kwargs):
        self._temporal_value_function = value_function(self.tick, **kwargs)

    def to_time_coordinate(self):
        return TimeCoordinate(self.location.x, self.location.y, self.location.z, self.tick)

    def clone(self):
        return PointOfInterest(self.location.clone(), self.tick)
