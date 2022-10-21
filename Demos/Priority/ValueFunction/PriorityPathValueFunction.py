from typing import List, TYPE_CHECKING

from Simulator import ValueFunction

if TYPE_CHECKING:
    from Simulator import PathAgent, Segment

violationValue = - 20


class PriorityPathValueFunction(ValueFunction):
    label = "PrioPath"
    description = "Magic"

    def value_for_segments(self, segments: List["Segment"], agent: "PathAgent"):
        """
        This Value function is not realistic and purely to produce illustrative results.
        To truly compare mechanisms a scenario dependant value function is needed
        :param segments:
        :param agent:
        :return:
        """
        if len(segments) == 0:
            return 0.

        if len(segments) != len(agent.locations) - 1:
            print(f"Crash {agent}: Not all locations reached")
            return violationValue

        expected_distance = 0
        _iter = agent.locations[0]
        for location in agent.locations[1:]:
            expected_distance += _iter.distance(location) * 1.1
            _iter = location
        value = expected_distance * 2 * agent.config["priority"]
        time = 0
        for path, location in zip(segments, agent.locations[1:]):
            destination = path.max
            if not destination.inter_temporal_equal(location):
                print(f"Crash {agent}: no further path found")
                return violationValue

            time += destination.t - path.min.t
            value -= max(destination.t - location.t, 0) / 100

        if time > agent.battery:
            print(f"Crash {self}: empty battery")
            return violationValue

        return round(max(0., value), 2)
