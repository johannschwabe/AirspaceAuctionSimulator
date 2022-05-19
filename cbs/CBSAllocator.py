"""

Python implementation of Conflict-based search

author: Ashwin Bose (@atb033)

"""
import sys
from typing import List, Dict

from .CBSPathFinding import astar
from Simulator import Environment
from Simulator.Agent import Agent
from Simulator.Allocator import Allocator
from Simulator.Coordinate import Coordinate, TimeCoordinate
from .CBSHelpers import HighLevelNode, Constraints, Conflict, VertexConstraint, EdgeConstraint
from multiprocessing import Process, Pool

sys.path.insert(0, '../Simulator/')




class CBS(Allocator):
    def allocate_for_agents(self, agents: List[Agent], env: Environment) -> Dict[Agent, List[List[TimeCoordinate]]]:
        open_set = set()
        closed_set = set()
        constraints_dict = {}
        start = HighLevelNode()
        start.constraint_dict = {}
        for agent in agents:
            start.constraint_dict[agent] = Constraints()
        start.solution = self.compute_solution(env, agents, constraints_dict)
        if not start.solution:
            return {}
        start.cost = self.compute_solution_cost(start.solution)

        open_set |= {start}

        while open_set:
            P = min(open_set)
            open_set -= {P}
            closed_set |= {P}

            constraint_dict = P.constraint_dict
            conflict_dict = self.get_first_conflict(P.solution)
            if not conflict_dict:
                print("solution found")
                self.get_first_conflict(P.solution)
                return CBS.generate_plan(P.solution)

            constraint_dict = self.create_constraints_from_conflict(conflict_dict)

            for agent in constraint_dict.keys():
                new_node = P.copy()
                new_node.constraint_dict[agent].add_constraint(constraint_dict[agent])

                new_node.solution = self.compute_solution(env, agents, new_node.constraint_dict)
                if not new_node.solution:
                    print("Failure")
                    continue
                new_node.cost = self.compute_solution_cost(new_node.solution)

                # TODO: ending condition
                if new_node not in closed_set:
                    open_set |= {new_node}

        return {}

    @staticmethod
    def generate_plan(solution):
        res = {}
        for agent, path in solution.items():
            res[agent] = [path]
        return res

    @staticmethod
    def compute_solution(env, agents, constraint_dict):
        solution = {}

        with Pool(len(agents)) as p:
            _solutions = p.map(CBS.parallelAstar, [(agent, constraint_dict.setdefault(agent, Constraints()), env) for agent in agents])
        for agent, local_solution in zip(agents, _solutions):
            if not local_solution:
                return False
            solution.update({agent: local_solution})
        return solution

    @staticmethod
    def parallelAstar(args):
        agent, constraint, env = args
        bid = agent.get_bid()
        local_solution = astar(bid.a, bid.b, env, agent, constraint)
        if not local_solution:
            return False
        return local_solution

    @staticmethod
    def compute_solution_cost(solution):
        return sum([len(path) for path in solution.values()])

    def get_first_conflict(self, solution):
        start = min([plan[0].t for plan in solution.values()])
        max_t = max([plan[-1].t for plan in solution.values()])
        result = Conflict()
        agents = list(solution.keys())
        for t in range(start, max_t):
            posis = []
            count = 0
            for agent in agents:
                position = self.get_state(agent, solution, t)
                if position == -1:
                    count += 1
                    continue
                adjacent =  next(filter(lambda  posi: abs(posi.x - position.x) <= 1 and abs(posi.y - position.y) <= 1 and abs(posi.z - position.z) <= 1 , posis ), None)
                if adjacent:
                    print(t)
                    result.time = t
                    result.type = Conflict.VERTEX
                    result.location_1 = position
                    result.location_2 = adjacent
                    result.agent_1 = agent
                    result.agent_2 = agents[posis.index(adjacent) + count]
                    return result
                else:
                    posis.append(position)
            for index, agent  in enumerate(agents):
                position = self.get_state(agent, solution, t + 1)
                if position == -1:
                    continue
                cpy = position.clone()
                cpy.t -= agent.speed
                if cpy in posis and posis.index(cpy) != index:
                    print(t)
                    result.time = t
                    result.type = Conflict.EDGE
                    result.location_1 = cpy
                    result.location_2 = position
                    result.agent_1 = agents[posis.index(cpy)]
                    result.agent_2 = agent
                    return result

        return False

    @staticmethod
    def get_state(agent_name, solution, t):
        if solution[agent_name][0].t < t < solution[agent_name][-1].t:
            return solution[agent_name][t - solution[agent_name][0].t]
        else:
            return -1


    @staticmethod
    def create_constraints_from_conflict(conflict):
        constraint_dict = {}
        if conflict.type == Conflict.VERTEX:
            constraint_1 = Constraints()
            constraint_2 = Constraints()

            v_constraint_1 = VertexConstraint(conflict.location_1)
            v_constraint_2 = VertexConstraint(conflict.location_2)
            constraint_1.vertex_constraints |= {v_constraint_1}
            constraint_2.vertex_constraints |= {v_constraint_2}
            constraint_dict[conflict.agent_1] = constraint_1
            constraint_dict[conflict.agent_2] = constraint_2

        elif conflict.type == Conflict.EDGE:
            constraint1 = Constraints()
            constraint2 = Constraints()

            e_constraint1 = EdgeConstraint(conflict, conflict)
            e_constraint2 = EdgeConstraint( conflict, conflict)

            constraint1.edge_constraints |= {e_constraint1}
            constraint2.edge_constraints |= {e_constraint2}

            constraint_dict[conflict.agent_1] = constraint1
            constraint_dict[conflict.agent_2] = constraint2

        return constraint_dict
