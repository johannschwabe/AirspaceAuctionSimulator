from typing import Dict, TYPE_CHECKING, Set, List

if TYPE_CHECKING:
    from Simulator.Agents.PathAgent import PathAgent
    from Simulator.Agents.Agent import Agent
    from Simulator.Coordinates.Coordinate4D import Coordinate4D


class Conflict(object):
    def __init__(self, agent_1: "PathAgent", agent_2: "PathAgent", location_1: "Coordinate4D",
                 location_2: "Coordinate4D"):
        self.agent_1: "PathAgent" = agent_1
        self.agent_2: "PathAgent" = agent_2

        self.location_1: "Coordinate4D" = location_1
        self.location_2: "Coordinate4D" = location_2

    def __str__(self):
        return '(' + str(self.agent_1) + ', ' + str(self.agent_2) + \
               ', ' + str(self.location_1) + ', ' + str(self.location_2) + ')'


class Constraints(object):
    def __init__(self, constraints: Set["Coordinate4D"] | None = None):
        self.constraints: Set["Coordinate4D"] = constraints if constraints else set()

    def add_constraint(self, other):
        self.constraints |= other.constraints

    def __str__(self):
        return "Constraints: " + str([str(vc) for vc in self.constraints])

    def copy(self):
        cpy = Constraints()
        cpy.constraints = self.constraints.copy()
        return cpy


class HighLevelNode(object):
    def __init__(self):
        self.solution: Dict["Agent", List["Coordinate4D"]] = dict()
        self.constraint_dict: Dict["Agent", "Constraints"] = dict()
        self.cost = 0

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.solution == other.solution and self.cost == other.cost

    def __hash__(self):
        return hash(str(self.cost) + ','.join(
            [str(agent) + str(constraints) for agent, constraints in self.constraint_dict.items()]))

    def __lt__(self, other):
        return self.cost < other.cost

    def copy(self):
        cpy = HighLevelNode()
        cpy.cost = self.cost
        for agent in list(self.constraint_dict.keys()):
            cpy.constraint_dict[agent] = self.constraint_dict[agent].copy()
        for agent in self.solution.keys():
            cpy.solution[agent] = self.solution[agent]
        return cpy
