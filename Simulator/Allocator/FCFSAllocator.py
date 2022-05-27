from typing import List, Dict

from ..Path import PathSegment, SpaceSegment
from ..Time import Tick
from ..Environment import Environment
from ..Agent import Agent, PathAgent
from ..Allocator import Allocator
from ..Bid import ABBid, Bid, ABABid, StationaryBid, ABCBid
from ..Coordinate import TimeCoordinate
from ..helpers.PathFinding import astar


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agents(self, agents: List[Agent], env: Environment, tick: Tick) -> Dict[Agent, List[List[TimeCoordinate]]]:
        res = {}
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
                    res[agent] = []
                    continue

                optimal_path_segments.append(PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path))

                # A-B-A
                if isinstance(bid, ABABid):
                    b = ab_path[-1]
                    ba_path = astar(
                        TimeCoordinate(b.x, b.y, b.z, b.t + Tick(bid.stay)),
                        bid.a2,
                        env,
                        agent,
                    )

                    if len(ba_path) == 0 or ab_path[-1].t - ab_path[0].t + ba_path[-1].t - ba_path[0].t > agent.battery:
                        res[agent] = []
                        continue

                    optimal_path_segments.append(PathSegment(bid.b.to_inter_temporal(), bid.a.to_inter_temporal(), 1, ba_path))
                res[agent] = optimal_path_segments
                env.allocate_path_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)

            elif isinstance(bid, StationaryBid):
                path = []
                for t in range(bid.start_t, bid.end_t + 1):
                    path_t = []
                    occupied = False
                    for coordinate in bid.block:
                        time_coord = TimeCoordinate(coordinate.x, coordinate.y, coordinate.z, Tick(t))
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
                res[agent] = optimal_path_segments
                env.allocate_spaces_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)
            elif isinstance(bid, ABCBid):
                a = bid.locations[0]
                time = 0
                for b, stay in zip(bid.locations[1:], bid.stays + [0]):
                    ab_path = astar(
                        a,
                        b,
                        env,
                        agent,
                    )

                    if len(ab_path) == 0:
                        break

                    time += ab_path[-1].t - ab_path[0].t
                    if time > agent.battery:
                        break

                    optimal_path_segments.append(ab_path)
                    a = b

                res[agent] = optimal_path_segments
                env.allocate_path_for_agent(agent, optimal_path_segments)
                env.add_agent(agent)
        return res
