from time import time_ns

from AAS import Allocator, AStar, AgentType, PathSegment
from Demos.FCFS.Owners.FCFSABAOwner import FCFSABAOwner
from Demos.FCFS.Owners.FCFSABCOwner import FCFSABCOwner
from Demos.FCFS.Owners.FCFSABOwner import FCFSABOwner
from Demos.FCFS.Owners.FCFSStationaryOwner import FCFSStationaryOwner


class FCFSAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [FCFSABOwner, FCFSABAOwner, FCFSABCOwner, FCFSStationaryOwner]

    def __init__(self):
        super().__init__()

    def allocate_ab(self, agent, bid, astar):
        ab_path, _ = astar.astar(
            bid.a,
            bid.b,
            agent,
        )

        if len(ab_path) == 0 or ab_path[-1].t - ab_path[0].t > agent.battery:
            return None

        optimal_path_segments = [PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)]
        return optimal_path_segments

    def allocate_aba(self, agent, bid, astar):
        ab_path, _ = astar.astar(
            bid.a,
            bid.b,
            agent,
        )
        b = ab_path[-1].clone()
        b.t += bid.stay
        ba_path, _ = astar.astar(
            b.
            bid.a2,
            agent,
        )

        if len(ab_path) == 0 or len(ba_path) == 0 or ab_path[-1].t - ab_path[0].t + ba_path[-1].t - ba_path[
            0].t > agent.battery:
            return None

        optimal_path_segments = [
            PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path),
            PathSegment(bid.b.to_inter_temporal(), bid.a.to_inter_temporal(), 1, ba_path)
        ]
        return optimal_path_segments

    def allocate_abc(self, agent, bid, astar):
        a = bid.locations[0]
        time = 0
        count = 0
        optimal_path_segments = []
        for b, stay in zip(bid.locations[1:], bid.stays):
            ab_path, _ = astar.astar(
                a,
                b,
                agent,
            )

            if len(ab_path) == 0:
                return None

            time += ab_path[-1].t - ab_path[0].t
            if time > agent.battery:
                return None

            optimal_path_segments.append(
                PathSegment(a.to_inter_temporal(), b.to_inter_temporal(), count, ab_path))
            count += 1
            a = ab_path[-1].clone()

        return optimal_path_segments

    def allocate_for_agents(self,
                            agents,
                            environment,
                            tick):
        astar = AStar(environment)
        allocations = []
        for agent in agents:
            start_time = time_ns()
            optimal_path_segments = []
            bid = agent.get_bid(tick)

            if agent.allocation_type == AllocationType.PATH:
                # A-B
                if agent.agent_type == AgentType.AB:
                    optimal_path_segments = self.allocate_ab(agent, bid, astar)

                # A-B-A
                elif agent.agent_type == AgentType.ABA:
                    optimal_path_segments = self.allocate_aba(agent, bid, astar)

                # A-B-C
                elif agent.agent_type == AgentType.ABC:
                    optimal_path_segments = self.allocate_abc(agent, bid, astar)

                environment.allocate_path_for_agent(agent, optimal_path_segments)
                environment.add_agent(agent)
                allocations.append(PathAllocation(agent,
                                                  optimal_path_segments,
                                                  AllocationReason(str(Reason.FIRST_ALLOCATION.value)),
                                                  (time_ns() - start_time) / 1e6)
                                   )
            # Stationary
            elif agent.agent_type == AgentType.STATIONARY:

                for block in bid.blocks:
                    block_valid = environment.is_box_valid_for_allocation(block[0], block[1], agent)
                    if block_valid:
                        optimal_path_segments.append(SpaceSegment(block[0], block[1]))

                environment.allocate_spaces_for_agent(agent, optimal_path_segments)
                environment.add_agent(agent)
                allocations.append(SpaceAllocation(agent,
                                                   optimal_path_segments,
                                                   AllocationReason(str(Reason.FIRST_ALLOCATION.value)),
                                                   (time_ns() - start_time) / 1e6)
                                   )
        return allocations
