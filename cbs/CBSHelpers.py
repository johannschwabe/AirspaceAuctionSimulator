from Simulator.Coordinate import Coordinate


class Location(object):
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return str((self.x, self.y))

class State(object):
    def __init__(self, time, location):
        self.time = time
        self.location = location
    def __eq__(self, other):
        return self.time == other.time and self.location == other.location
    def __hash__(self):
        return hash(str(self.time)+str(self.location.x) + str(self.location.y))
    def is_equal_except_time(self, state):
        return self.location == state.location
    def __str__(self):
        return str((self.time, self.location.x, self.location.y))

class Conflict(object):
    VERTEX = 1
    EDGE = 2
    def __init__(self):
        self.time = -1
        self.type = -1

        self.agent_1 = ''
        self.agent_2 = ''

        self.location_1 = Coordinate(0,0,0)
        self.location_2 = Coordinate(0,0,0)

    def __str__(self):
        return '(' + str(self.time) + ', ' + str(self.agent_1) + ', ' + str(self.agent_2) + \
             ', '+ str(self.location_1) + ', ' + str(self.location_2) + ')'

class VertexConstraint(object):
    def __init__(self, location):
        self.location = location

    def __eq__(self, other):
        return self.location == other.location
    def __hash__(self):
        return hash(str(self.location))
    def __str__(self):
        return '(' + str(self.location) + ')'

class EdgeConstraint(object):
    def __init__(self, timeCord_1, timeCord_2):
        self.location_1 = timeCord_1
        self.location_2 = timeCord_2
    def __eq__(self, other):
        return self.location_1 == other.location_1 \
            and self.location_2 == other.location_2
    def __hash__(self):
        return hash(str(self.location_1) + str(self.location_2))
    def __str__(self):
        return '(' + str(self.location_1) +', '+ str(self.location_2) + ')'

class Constraints(object):
    def __init__(self):
        self.vertex_constraints = set()
        self.edge_constraints = set()

    def add_constraint(self, other):
        self.vertex_constraints |= other.vertex_constraints
        self.edge_constraints |= other.edge_constraints

    def __str__(self):
        return "VC: " + str([str(vc) for vc in self.vertex_constraints])  + \
            "EC: " + str([str(ec) for ec in self.edge_constraints])

    def copy(self):
        cpy = Constraints()
        cpy.vertex_constraints = self.vertex_constraints.copy()
        cpy.edge_constraints = self.edge_constraints.copy()
        return cpy

class HighLevelNode(object):
    def __init__(self):
        self.solution = dict()
        self.constraint_dict = dict()
        self.cost = 0

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.solution == other.solution and self.cost == other.cost

    def __hash__(self):
        return hash(str(self.cost) + ','.join([str(agent)+str(constraints) for agent, constraints in self.constraint_dict.items()]))

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
