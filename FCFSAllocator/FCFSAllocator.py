from typing import List

from Simulator.Enum import Reason
from Simulator.Path import PathSegment, SpaceSegment, PathReallocation, SpaceReallocation
from Simulator.Environment import Environment
from Simulator.Agent import Agent, PathAgent, SpaceAgent
from Simulator.Allocator import Allocator
from Simulator.Bid import ABBid, Bid, ABABid, StationaryBid, ABCBid
from Simulator.Coordinate import Coordinate4D
from Simulator.helpers.PathFinding import astar


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agents(self,
                            agents: List[Agent],
                            env: Environment,
                            tick: int) -> List[SpaceReallocation | PathReallocation]:
        res = []
        for agent in agents:
            optimal_path_segments: List[PathSegment|SpaceSegment] = []
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
                    res.append(PathReallocation(agent, [], Reason.ALLOCATION_FAILED))
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
                        res.append(PathReallocation(agent, [], Reason.ALLOCATION_FAILED))
                        continue

                    optimal_path_segments.append(PathSegment(bid.b.to_inter_temporal(), bid.a.to_inter_temporal(), 1, ba_path))

                res.append(PathReallocation(agent, optimal_path_segments, Reason.FIRST_ALLOCATION))

                env.allocate_path_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)

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

                res.append(PathReallocation(agent, optimal_path_segments, Reason.FIRST_ALLOCATION))
                env.allocate_path_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)

            elif isinstance(bid, StationaryBid) and isinstance(agent, SpaceAgent):
                path = []
                for t in range(bid.start_t, bid.end_t + 1):
                    path_t = []
                    occupied = False
                    for coordinate in bid.block:
                        time_coord = Coordinate4D(coordinate.x, coordinate.y, coordinate.z, t)
                        if env.is_valid_for_allocation(time_coord, agent):
                            path_t.append(time_coord)
                        else:
                            occupied = True
                            break

                    if not occupied:
                        path += path_t
                    else:
                        if len(path) > 0:
                            optimal_path_segments.append(path)
                        path = []

                if len(path) > 0:
                    optimal_path_segments.append(path)
                res.append(SpaceReallocation(agent, optimal_path_segments, Reason.FIRST_ALLOCATION))
                env.allocate_spaces_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)
        return res
