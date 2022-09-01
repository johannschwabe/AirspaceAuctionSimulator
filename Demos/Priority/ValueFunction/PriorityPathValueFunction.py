from typing import List, TYPE_CHECKING

from Simulator import ValueFunction

if TYPE_CHECKING:
    from Simulator import PathAgent, Segment


class PriorityPathValueFunction(ValueFunction):
    label = "PrioPath"
    description = "Magic"

    def __init__(self, config):
        super().__init__(config)

    def value_for_segments(self, segments: List["Segment"], agent: "PathAgent"):
        if len(segments) == 0:
            return 0.

        if len(segments) != len(agent.locations) - 1:
            print(f"Crash {agent}: Not all locations reached")
            return -1.

        value = 1.
        time = 0
        for path, location in zip(segments, agent.locations[1:]):
            destination = path.max
            if not destination.inter_temporal_equal(location):
                print(f"Crash {agent}: no further path found")
                return -1.

            time += destination.t - path.min.t
            value -= max(destination.t - location.t, 0) / 100

        if time > agent.battery:
            print(f"Crash {self}: empty battery")
            return -1.

        return round(max(0., value), 2)
