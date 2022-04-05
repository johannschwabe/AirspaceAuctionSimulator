from typing import List, Dict

from ..Time import Tick
from ..Environment import Environment
from ..Agent import Agent
from ..Allocator import Allocator
from ..Bid import ABBid, Bid, ABABid, BlockerBid, ABCBid
from ..Coordinate import TimeCoordinate
from ..helpers.PathFinding import astar


class FCFSAllocator(Allocator):
    def __init__(self):
        super().__init__()

    def allocate_for_agents(self, agents: List[Agent], env: Environment) -> Dict[Agent, List[List[TimeCoordinate]]]:
        res = {}
        for agent in agents:
            optimal_paths: List[List[TimeCoordinate]] = []
            bid: Bid = agent.get_bid()

            # A-B
            if isinstance(bid, ABBid):
                ab_path = astar(
                    bid.a,
                    bid.b,
                    env,
                    agent,
                )
                if len(ab_path) == 0 or ab_path[-1].t - ab_path[0].t > agent.battery:
                    res[agent] = []
                    continue

                optimal_paths.append(ab_path)

                # A-B-A
                if isinstance(bid, ABABid):
                    b = ab_path[-1]
                    ba_path = astar(
                        TimeCoordinate(b.x, b.y, b.z, b.t + Tick(bid.stay)),
                        bid.a,
                        env,
                        agent,
                    )

                    if len(ba_path) == 0 or ab_path[-1].t - ab_path[0].t + ba_path[-1].t - ba_path[0].t > agent.battery:
                        res[agent] = []
                        continue

                    optimal_paths.append(ba_path)
                res[agent] = optimal_paths
                env.allocate_paths_for_agent(agent, optimal_paths)
                env.add_agent(agent)

            elif isinstance(bid, BlockerBid):
                path = []
                for t in range(bid.start_t, bid.end_t + 1):
                    path_t = []
                    occupied = False
                    for coordinate in bid.block:
                        time_coord = TimeCoordinate(coordinate.x, coordinate.y, coordinate.z, Tick(t))
                        field = env.get_field_at(time_coord, False)
                        if field.is_allocated() or field.is_near():
                            occupied = True
                            break
                        else:
                            path_t.append(time_coord)

                    if not occupied:
                        path += path_t
                    else:
                        if len(path) > 0:
                            optimal_paths.append(path)
                        path = []

                if len(path) > 0:
                    optimal_paths.append(path)
                res[agent] = optimal_paths
                env.allocate_paths_for_agent(agent, optimal_paths)
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

                    optimal_paths.append(ab_path)
                res[agent] = optimal_paths
                env.allocate_paths_for_agent(agent, optimal_paths)
                env.add_agent(agent)
        return res
