"""
Python implementation of Conflict-based search
author: Ashwin Bose (@atb033)
"""
from typing import List, Dict, TYPE_CHECKING, Set, Type, Iterator

from rtree import Index
from rtree.index import Property

from Simulator.Agents.PathAgent import PathAgent
from Simulator.Allocations.Allocation import Allocation
from Simulator.Allocations.AllocationHistory import AllocationHistory
from Simulator.Allocations.AllocationReason import AllocationReason
from Simulator.Mechanism.Allocator import Allocator
from Simulator.Segments.PathSegment import PathSegment
from .CBSAllocatorHelpers import HighLevelNode, Constraints, Conflict
from ..BidTracker.CBSBidTracker import CBSBidTracker
from ..BiddingStrategy.CBSPathBiddingStrategy import CBSPathBiddingStrategy
from ..Bids.CBSPathBid import CBSPathBid
from ..CBSAstar.CBSAstar import AStar, find_valid_path_tick
from ..PaymentRule.CBSPaymentRule import CBSPaymentRule

if TYPE_CHECKING:
    from Simulator.BidTracker.BidTracker import BidTracker
    from Simulator.Agents.Agent import Agent
    from Simulator.Environment.Environment import Environment


class CBS(Allocator):

    @staticmethod
    def compatible_bidding_strategies() -> List[Type["CBSPathBiddingStrategy"]]:
        return [CBSPathBiddingStrategy]

    @staticmethod
    def compatible_payment_functions():
        return [CBSPaymentRule]

    def __init__(self):
        self.bid_tracker = CBSBidTracker()

    def get_bid_tracker(self) -> "BidTracker":
        return self.bid_tracker

    def allocate(self, agents: List["PathAgent"], env: "Environment", tick: int) -> Dict["Agent", "Allocation"]:
        open_set: Set["HighLevelNode"] = set()
        closed_set = set()
        constraints_dict: Dict[int, "Constraints"] = {}
        start = HighLevelNode()
        start.constraint_dict = {}
        for agent in agents:
            start.constraint_dict[hash(agent)] = Constraints()
        _solution = self.compute_solution(env, agents, constraints_dict, tick)
        if not _solution:
            return {}
        start.solution = _solution
        start.cost = self.compute_solution_cost(start.solution)

        open_set |= {start}

        while open_set:
            P = min(open_set)
            open_set -= {P}
            closed_set |= {P}

            first_conflict = CBS.get_first_conflict(P.solution, env.max_near_radius)
            if not first_conflict:
                print("solution found")
                allocations = {}
                for agent, path in P.solution.items():
                    allocations[agent] = Allocation(agent, path, AllocationHistory(
                        self.bid_tracker.get_last_bid_for_tick(tick, agent, env), 0, AllocationReason.FIRST_ALLOCATION,
                        "CBS Allocation"))
                return allocations

            constraint_dict = self.create_constraints_from_conflict(first_conflict)

            for agent in constraint_dict.keys():
                new_node = P.copy()
                new_node.constraint_dict[hash(agent)].add_constraint(constraint_dict[agent])
                print(str(new_node))
                new_node.solution = self.compute_solution(env, agents, new_node.constraint_dict, tick)
                if not new_node.solution:
                    print("Failure")
                    continue
                new_node.cost = self.compute_solution_cost(new_node.solution)

                # TODO: ending condition
                if new_node not in closed_set:
                    open_set |= {new_node}

        return {}

    def compute_solution(self,
                         env,
                         agents: List["PathAgent"],
                         constraint_dict: Dict[int, "Constraints"],
                         tick: int) -> Dict["PathAgent", List["PathSegment"]]:
        solution = {}
        _solutions = [CBS.parallel_astar(
            (agent, self.bid_tracker.get_last_bid_for_tick(0, agent, env), constraint_dict, env, tick)) for agent in
            agents]
        # with Pool(len(agents)) as p:
        #     _solutions = p.map(CBS.parallelAstar,
        #                        [(agent, constraint_dict.setdefault(agent, Constraints()), env) for agent in agents])
        for agent, local_solution in zip(agents, _solutions):
            if not local_solution:
                return {}
            solution.update({agent: local_solution})
        return solution

    @staticmethod
    def parallel_astar(args) -> List[PathSegment] | None:
        agent, bid, constraints_dict, env, tick = args
        assert isinstance(bid, CBSPathBid) and isinstance(agent, PathAgent)
        valid_t = find_valid_path_tick(env, bid.locations[0], agent, 0, env.dimension.t, constraints_dict)
        start = bid.locations[0].clone()
        start.t = valid_t
        astar = AStar(env)
        local_solution = astar.astar(start, bid.locations[1], agent, constraints_dict)
        if len(local_solution) == 0:
            return None

        return [PathSegment(bid.locations[0].to_3D(), bid.locations[1].to_3D(), 0, local_solution)]

    @staticmethod
    def compute_solution_cost(solution):
        return sum([sum([len(path.coordinates) for path in paths]) for paths in solution.values()])

    @staticmethod
    def get_first_conflict(solution: Dict["PathAgent", List["PathSegment"]], max_near_radius: float):
        props = Property()
        props.dimension = 4
        tree = Index(properties=props)
        start_t = min([plan[0].min.t for plan in solution.values()])
        max_t = max([plan[-1].max.t for plan in solution.values()])
        agents: Dict[int, "PathAgent"] = {hash(agent): agent for agent in solution.keys()}
        new_max_near_radius = max([max_near_radius] + [agent.near_radius for agent in agents.values()])
        for t in range(start_t, max_t):
            for _agent in agents.values():
                if len(solution[_agent]) > 0 and 0 <= t - solution[_agent][0].min.t < len(
                    solution[_agent][0].coordinates):
                    posi = solution[_agent][0].coordinates[t - solution[_agent][0].min.t]
                    bl = posi - new_max_near_radius
                    tr = posi + new_max_near_radius
                    intersections: Iterator[int] = tree.intersection(bl.list_rep() + tr.list_rep())
                    intersecting_agents = set(
                        [agents[agent_hash] for agent_hash in intersections if agent_hash != hash(_agent)])
                    for intersecting_agent in intersecting_agents:
                        local_max_near_radius = max(_agent.near_radius, intersecting_agent.near_radius)
                        path_coordinate = solution[intersecting_agent][0].coordinates[
                            t - solution[intersecting_agent][0].min.t]
                        distance = posi.distance(path_coordinate, l2=True)
                        if distance <= local_max_near_radius:
                            return Conflict(_agent, intersecting_agent, posi, path_coordinate)
                    tree.insert(hash(_agent), posi.list_rep())
        return False

    @staticmethod
    def get_state(agent_name, solution, t):
        if solution[agent_name][0].t < t < solution[agent_name][-1].t:
            return solution[agent_name][t - solution[agent_name][0].t]
        else:
            return -1

    @staticmethod
    def create_constraints_from_conflict(conflict: "Conflict") -> Dict["Agent", "Constraints"]:
        constraint_dict = {}

        constraints_1 = Constraints({conflict.location_1})
        constraints_2 = Constraints({conflict.location_2})

        constraint_dict[conflict.agent_1] = constraints_1
        constraint_dict[conflict.agent_2] = constraints_2

        return constraint_dict
