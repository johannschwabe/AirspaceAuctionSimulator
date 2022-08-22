from time import time_ns

from Demos.FCFS.Owners.FCFSABAOwner import FCFSABAOwner
from Demos.FCFS.Owners.FCFSABCOwner import FCFSABCOwner
from Demos.FCFS.Owners.FCFSABOwner import FCFSABOwner
from Demos.FCFS.Owners.FCFSStationaryOwner import FCFSStationaryOwner
from Simulator import \
    Allocator, \
    AStar, \
    AgentType, \
    PathSegment, \
    SpaceSegment, \
    AllocationType, \
    PathAllocation, \
    SpaceAllocation, \
    AllocationReason


class FCFSAllocator(Allocator):
    @staticmethod
    def compatible_owner():
        return [FCFSABOwner, FCFSABAOwner, FCFSABCOwner, FCFSStationaryOwner]

    def __init__(self):
        super().__init__()

    @staticmethod
    def allocate_ab(agent, bid, astar):
        ab_path, _ = astar.astar(
            bid.a,
            bid.b,
            agent,
        )

        if len(ab_path) == 0 or ab_path[-1].t - ab_path[0].t > agent.battery:
            return None

        optimal_path_segments = [PathSegment(bid.a.to_inter_temporal(), bid.b.to_inter_temporal(), 0, ab_path)]
        return optimal_path_segments

    @staticmethod
    def allocate_aba(agent, bid, astar):
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

    @staticmethod
    def allocate_abc(agent, bid, astar):
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

    @staticmethod
    def allocate_stationary(agent, bid, environment):
        optimal_path_segments = []
        for block in bid.blocks:
            block_valid = environment.is_space_valid_for_allocation(block[0], block[1], agent)
            if block_valid:
                optimal_path_segments.append(SpaceSegment(block[0], block[1]))
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

            # Allocation Agents
            if agent.allocation_type == AllocationType.PATH.value:
                match agent.agent_type:
                    # A-B
                    case AgentType.AB.value:
                        optimal_path_segments = self.allocate_ab(agent, bid, astar)
                    # A-B-A
                    case AgentType.ABA.value:
                        optimal_path_segments = self.allocate_aba(agent, bid, astar)
                    # A-B-C
                    case AgentType.ABC.value:
                        optimal_path_segments = self.allocate_abc(agent, bid, astar)

                if optimal_path_segments is None:
                    allocations.append(
                        PathAllocation(agent, [], str(AllocationReason.ALLOCATION_FAILED.value),
                                       compute_time=time_ns() - start_time))
                    continue

                environment.allocate_path_for_agent(agent, optimal_path_segments)
                allocations.append(PathAllocation(agent,
                                                  optimal_path_segments,
                                                  str(AllocationReason.FIRST_ALLOCATION.value),
                                                  compute_time=time_ns() - start_time))

            # Space Agents
            elif agent.allocation_type == AllocationType.SPACE.value:
                match agent.agent_type:
                    # Stationary
                    case AgentType.STATIONARY.value:
                        optimal_path_segments = self.allocate_stationary(agent, bid, environment)

                environment.allocate_space_for_agent(agent, optimal_path_segments)
                allocations.append(SpaceAllocation(agent,
                                                   optimal_path_segments,
                                                   str(AllocationReason.FIRST_ALLOCATION.value),
                                                   compute_time=time_ns() - start_time))

            environment.add_agent(agent)
        return allocations
