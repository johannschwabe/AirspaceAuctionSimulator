"""
Python implementation of Conflict-based search
author: Ashwin Bose (@atb033)
"""
from typing import List, Dict, TYPE_CHECKING, Set, Type, Iterator, Tuple, Optional

from rtree import Index
from rtree.index import Property

from Simulator.Agents.PathAgent import PathAgent
from Simulator.Allocations.Allocation import Allocation
from Simulator.Allocations.AllocationHistory import AllocationHistory
from Simulator.Allocations.AllocationReason import AllocationReason
from Simulator.Mechanism.Allocator import Allocator
from Simulator.Segments.PathSegment import PathSegment
from .CBSAllocatorHelpers import HighLevelNode, Conflict
from .CBSCostFunctions import PathLength, CostFunction
from ..BidTracker.CBSBidTracker import CBSBidTracker
from ..BiddingStrategy.CBSPathBiddingStrategy import CBSPathBiddingStrategy
from ..Bids.CBSPathBid import CBSPathBid
from ..CBSAstar.CBSAstar import CBSAStar, find_valid_path_tick
from ..PaymentRule.CBSPaymentRule import CBSPaymentRule

if TYPE_CHECKING:
    from Simulator.Coordinates.Coordinate4D import Coordinate4D
    from Simulator.BidTracker.BidTracker import BidTracker
    from Simulator.Environment.Environment import Environment


class CBS(Allocator):

    @staticmethod
    def compatible_bidding_strategies() -> List[Type["CBSPathBiddingStrategy"]]:
        return [CBSPathBiddingStrategy]

    @staticmethod
    def compatible_payment_functions():
        return [CBSPaymentRule]

    def __init__(self, cost_function: "CostFunction" = PathLength):
        self.bid_tracker = CBSBidTracker()
        self.cost_function = cost_function()

    def get_bid_tracker(self) -> "BidTracker":
        return self.bid_tracker

    def allocate(self, agents: List["PathAgent"], env: "Environment", tick: int) -> Dict["PathAgent", "Allocation"]:
        astar = CBSAStar(env)
        open_set: Set["HighLevelNode"] = set()
        closed_set: Set["HighLevelNode"] = set()
        start: "HighLevelNode" = HighLevelNode()
        start.constraint_dict = {}
        for _agent in agents:
            start.constraint_dict[_agent] = set()
            start.solution[_agent], start.reason = self.allocate_path(_agent, start.constraint_dict[_agent], env, tick,
                                                                      astar)
        for existing_agent in env.agents.values():
            assert isinstance(existing_agent, PathAgent)
            start.constraint_dict[existing_agent] = set()
            start.solution[existing_agent] = existing_agent.allocated_segments

        if not start.solution:
            return {}
        start.cost = self.cost_function(start)
        start.first_conflict = CBS.get_first_conflict(start.solution, env.max_near_radius)
        open_set |= {start}

        while open_set:
            P: "HighLevelNode" = min(open_set)
            open_set -= {P}
            closed_set |= {P}

            first_conflict = P.first_conflict
            if not first_conflict:
                allocations = {}
                for agent, path in P.solution.items():
                    allocations[agent] = Allocation(agent, path, AllocationHistory(
                        self.bid_tracker.get_last_bid_for_tick(tick, agent, env), 0, AllocationReason.FIRST_ALLOCATION,
                        "CBS Allocation"))
                return allocations

            constraint_dict = self.create_constraints_from_conflict(first_conflict)
            assert len(constraint_dict.keys()) == 2
            for _agent in constraint_dict.keys():
                new_node: "HighLevelNode" = P.copy()
                new_node.add_constraint(_agent, constraint_dict[_agent])
                if new_node not in closed_set:
                    self.compute_solution(env, new_node, tick, astar)
                    if not new_node.solution and not self.cost_function.failed_allocation_valid:
                        continue
                    open_set |= {new_node}

                    new_node.cost = self.cost_function(new_node)
                    new_node.first_conflict = CBS.get_first_conflict(new_node.solution, env.max_near_radius)
            P.solution = {}

        return {}

    def compute_solution(self,
                         env,
                         high_level_node: "HighLevelNode",
                         tick: int,
                         astar: "CBSAStar"):
        to_recompute = high_level_node.newly_constraint
        new_recomputed_solution, reason = self.allocate_path(to_recompute, high_level_node.constraint_dict, env, tick,
                                                             astar)
        if not new_recomputed_solution:
            high_level_node.solution = {}
            return
        high_level_node.solution[to_recompute] = new_recomputed_solution
        high_level_node.reason = reason
        return

    def allocate_path(self, agent, constraints_dict, env, tick, astar: "CBSAStar") -> Tuple[
        Optional[List["PathSegment"]], str]:
        bid = self.bid_tracker.get_last_bid_for_tick(tick, agent, env)
        assert isinstance(bid, CBSPathBid) and isinstance(agent, PathAgent)
        a = bid.locations[0].clone()
        start = a.to_3D()

        time = 0
        count = 0
        optimal_path_segments = []

        for _index, b in enumerate(bid.locations[1:]):

            end = b.to_3D()
            b = b.clone()

            if env.is_coordinate_blocked_forever(a, bid.agent.near_radius):
                return None, f"Static blocker at start {a}."

            if env.is_coordinate_blocked_forever(b, bid.agent.near_radius):
                return None, f"Static blocker at target {b}."

            a_t = find_valid_path_tick(env, a, agent, tick, env.dimension.t, constraints_dict)
            if a_t is None:
                return None, f"Start {a} is invalid until max tick {env.dimension.t}."
            a.t = a_t

            b_t = find_valid_path_tick(env, b, agent, tick, env.dimension.t, constraints_dict)
            if b_t is None:
                return None, f"Target {b} is invalid until max tick {env.dimension.t}."
            b.t = b_t

            ab_path = astar.astar(a, b, agent, constraints_dict)
            if len(ab_path) == 0:
                return None, f"No path {a} -> {b} found."
            time += ab_path[-1].t - ab_path[0].t
            if time > bid.battery:
                return None, f"Not enough battery left for path {a} -> {b}."

            optimal_path_segments.append(
                PathSegment(start, end, count, ab_path))

            count += 1

            a = ab_path[-1]
            start = a.to_3D()
            a = a.clone()
            if len(bid.stays) > _index:
                a.t += bid.stays[_index]
        return optimal_path_segments, "Path allocated."

    @staticmethod
    def get_first_conflict(solution: Dict["PathAgent", List["PathSegment"]], max_near_radius: float) -> "Conflict|None":
        props = Property()
        props.dimension = 4
        tree = Index(properties=props)
        start_t = min([plan[0].min.t for plan in solution.values()])
        max_t = max([plan[-1].max.t for plan in solution.values()])
        agents: Dict[int, "PathAgent"] = {hash(agent): agent for agent in solution.keys()}
        new_max_near_radius = max([max_near_radius] + [agent.near_radius for agent in agents.values()])
        for t in range(start_t, max_t):
            for _agent in agents.values():
                if len(solution[_agent]) > 0:
                    segment_index = 0
                    while len(solution[_agent]) > segment_index and solution[_agent][segment_index].min.t <= t:
                        if solution[_agent][segment_index].max.t >= t:
                            segment = solution[_agent][segment_index]
                            posi = segment.coordinates[t - segment.min.t]
                            bl = posi - new_max_near_radius
                            tr = posi + new_max_near_radius
                            intersections: Iterator[int] = tree.intersection(bl.list_rep() + tr.list_rep())
                            intersecting_agents = set(
                                [agents[agent_hash] for agent_hash in intersections if agent_hash != hash(_agent)])
                            for intersecting_agent in intersecting_agents:
                                local_max_near_radius = max(_agent.near_radius, intersecting_agent.near_radius)
                                path_coordinate = segment.coordinates[t - segment.min.t]
                                distance = posi.distance(path_coordinate, l2=True)
                                if distance <= local_max_near_radius:
                                    return Conflict(_agent, intersecting_agent, posi, path_coordinate)
                            tree.insert(hash(_agent), posi.list_rep())
                            break
                        segment_index += 1

        return None

    @staticmethod
    def get_state(agent_name, solution, t):
        if solution[agent_name][0].t < t < solution[agent_name][-1].t:
            return solution[agent_name][t - solution[agent_name][0].t]
        else:
            return -1

    @staticmethod
    def create_constraints_from_conflict(conflict: "Conflict") -> Dict["PathAgent", "Coordinate4D"]:
        return {conflict.agent_1: conflict.location_1, conflict.agent_2: conflict.location_2}
