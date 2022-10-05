from typing import Dict, TYPE_CHECKING, Set, List, Optional

if TYPE_CHECKING:
    from Simulator.Segments.PathSegment import PathSegment
    from Simulator.Agents.PathAgent import PathAgent
    from Simulator.Coordinates.Coordinate4D import Coordinate4D


class Conflict(object):
    """
    Structure to save two agents that got too close and their positions
    """

    def __init__(self, agent_1: "PathAgent", agent_2: "PathAgent", location_1: "Coordinate4D",
                 location_2: "Coordinate4D"):
        self.agent_1: "PathAgent" = agent_1
        self.agent_2: "PathAgent" = agent_2

        self.location_1: "Coordinate4D" = location_1
        self.location_2: "Coordinate4D" = location_2

    def __str__(self):
        return '(' + str(self.agent_1) + ', ' + str(self.agent_2) + \
               ', ' + str(self.location_1) + ', ' + str(self.location_2) + ')'


class HighLevelNode(object):
    """
    HighLevelNode for CBS. Saves a (possibly invalid) allocation for all agents and
    the constraints under which it was computed
    """

    def __init__(self):
        self.solution: Dict["PathAgent", List["PathSegment"]] = dict()
        self.constraint_dict: Dict["PathAgent", Set["Coordinate4D"]] = dict()
        self.first_conflict: "Optional[Conflict]" = None
        self.newly_constraint: "Optional[PathAgent]" = None
        self.reason: "str" = ""
        self.cost = 0

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.constraint_dict == other.constraint_dict

    def __hash__(self):
        return hash(','.join(
            [str(agent) + str(constraints) for agent, constraints in self.constraint_dict.items()]))

    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        if self.cost == other.cost:
            if not self.first_conflict:
                return True
            if not other.first_conflict:
                return False
            return self.first_conflict.location_1.t < other.first_conflict.location_1.t
        return self.cost < other.cost

    def add_constraint(self, agent: "PathAgent", constraint: "Coordinate4D"):
        self.constraint_dict[agent].add(constraint)
        self.newly_constraint = agent

    def copy(self):
        cpy = HighLevelNode()
        for agent in list(self.constraint_dict.keys()):
            cpy.constraint_dict[agent] = self.constraint_dict[agent].copy()
        for agent in list(self.solution.keys()):
            cpy.solution[agent] = self.solution[agent].copy()
        return cpy

    def __str__(self):
        res = ""
        for agent, constraint in self.constraint_dict.items():
            if len(constraint) > 0:
                res += f"{agent}: {str(constraint)}\n"
        return res
