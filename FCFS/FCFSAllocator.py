from time import time_ns
from typing import List

from Simulator.Owner.PathOwners.ABAOwner import ABAOwner
from Simulator.Owner.PathOwners.ABCOwner import ABCOwner
from Simulator.Owner.PathOwners.ABOwner import ABOwner
from Simulator.Owner.SpaceOwners.StationaryOwner import StationaryOwner
from Simulator.Path import PathSegment, SpaceSegment, PathReallocation, SpaceReallocation
from Simulator.Environment import Environment
from Simulator.Agent import Agent, PathAgent, SpaceAgent
from Simulator.Allocator import Allocator
from Simulator.Bid import ABBid, Bid, ABABid, StationaryBid, ABCBid
from Simulator.Coordinate import Coordinate4D
from Simulator.Path.AllocationReason import AllocationReason
from Simulator.Path.Reason import Reason
from Simulator.helpers.PathFinding import astar


class FCFSAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [ABOwner, ABAOwner, ABCOwner, StationaryOwner]

    def __init__(self):
        super().__init__()

    def allocate_for_agents(self,
                            agents: List[Agent],
                            env: Environment,
                            tick: int) -> List[SpaceReallocation | PathReallocation]:
        res = []
        for agent in agents:
            start_time = time_ns()
            optimal_path_segments: List[PathSegment | SpaceSegment] = []
            bid: Bid = agent.get_bid(tick)

            # A-B
            if isinstance(bid, ABBid) and isinstance(agent, PathAgent):
                ab_path = astar(
                    bid.a,
                    bid.b,
                    env,
                    agent,
                )
                if len(ab_path) == 0 or ab_path[-1].t - ab_path[0].t > agent.battery:
                    res.append(PathReallocation(agent, [], AllocationReason(str(Reason.ALLOCATION_FAILED.value))))
                    continue

                optimal_path_segments.append(PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path))

                # A-B-A
                if isinstance(bid, ABABid):
                    b = ab_path[-1]
                    ba_path = astar(
                        Coordinate4D(b.x, b.y, b.z, b.t + bid.stay),
                        bid.a2,
                        env,
                        agent,
                    )

                    if len(ba_path) == 0 or ab_path[-1].t - ab_path[0].t + ba_path[-1].t - ba_path[0].t > agent.battery:
                        res.append(PathReallocation(agent, [], AllocationReason(str(Reason.ALLOCATION_FAILED.value))))
                        continue

                    optimal_path_segments.append(PathSegment(bid.b.to_inter_temporal(), bid.a.to_inter_temporal(), 1, ba_path))

                env.allocate_path_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)
                res.append(PathReallocation(agent,
                                            optimal_path_segments,
                                            AllocationReason(str(Reason.FIRST_ALLOCATION.value)),
                                            (time_ns() - start_time)/1e6)
                           )

            elif isinstance(bid, ABCBid) and isinstance(agent, PathAgent):
                a = bid.locations[0]
                time = 0
                count = 0
                for b, stay in zip(bid.locations[1:], bid.stays):
                    ab_path = astar(
                        a,
                        b,
                        env,
                        agent,
                    )

                    if len(ab_path) == 0:
                        optimal_path_segments = []
                        break

                    time += ab_path[-1].t - ab_path[0].t
                    if time > agent.battery:
                        break

                    optimal_path_segments.append(PathSegment(a.to_inter_temporal(), b.to_inter_temporal(), count, ab_path))
                    count += 1
                    a = ab_path[-1].clone()

                env.allocate_path_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)
                res.append(PathReallocation(agent,
                                            optimal_path_segments,
                                            AllocationReason(str(Reason.FIRST_ALLOCATION.value)),
                                            (time_ns() - start_time)/1e6)
                           )

            elif isinstance(bid, StationaryBid) and isinstance(agent, SpaceAgent):

                for block in bid.blocks:
                    block_valid = env.is_box_valid_for_allocation(block[0], block[1], agent)
                    if block_valid:
                        optimal_path_segments.append(SpaceSegment(block[0], block[1]))

                env.allocate_spaces_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)
                res.append(SpaceReallocation(agent,
                                             optimal_path_segments,
                                             AllocationReason(str(Reason.FIRST_ALLOCATION.value)),
                                             (time_ns() - start_time)/1e6)
                           )
        return res
