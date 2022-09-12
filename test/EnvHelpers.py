import random

from Demos.FCFS.BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy
from Demos.FCFS.BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from Demos.FCFS.ValueFunction.FCFSPathValueFunction import FCFSPathValueFunction
from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Simulator import Allocation, AllocationType, AllocationStatistics, Coordinate4D, Coordinate3D, PathAgent, \
    PathSegment, SpaceAgent
from Simulator.Segments.SpaceSegment import SpaceSegment


def generate_path_agent():
    return PathAgent(f"AgentName{random.randint(0, 100000)}",
                     FCFSPathBiddingStrategy(),
                     FCFSPathValueFunction({}),
                     [Coordinate4D(2, 2, 2, 2), Coordinate4D(30, 30, 30, 30)],
                     [0], )


def generate_space_agent():
    return SpaceAgent(f"AgentName{random.randint(0, 100000)}",
                      FCFSSpaceBiddingStrategy(),
                      FCFSSpaceValueFunction({}),
                      [[Coordinate4D(40, 40, 40, 20), Coordinate4D(60, 60, 60, 70)]])


def generate_path_segment(base: Coordinate4D):
    start = base.to_inter_temporal()
    return PathSegment(start, start + Coordinate3D(3, 3, 3), 0, [
        base,
        base + Coordinate4D(0, 0, 1, 1),
        base + Coordinate4D(0, 0, 2, 2),
        base + Coordinate4D(0, 0, 2, 3),
        base + Coordinate4D(0, 1, 2, 4),
        base + Coordinate4D(1, 1, 2, 5),
        base + Coordinate4D(1, 1, 2, 6),
        base + Coordinate4D(2, 1, 2, 7),
        base + Coordinate4D(3, 1, 2, 8),
        base + Coordinate4D(3, 1, 3, 9),
        base + Coordinate4D(3, 2, 3, 10),
        base + Coordinate4D(3, 3, 3, 11),
    ])


def generate_space_segment(base: Coordinate4D):
    return SpaceSegment(base, base + Coordinate4D(10, 10, 10, 40))


def generate_allocation_statistics():
    return AllocationStatistics(500, AllocationType.FIRST_ALLOCATION, "first allocation", [])


def generate_path_allocation():
    agi = generate_path_agent()
    first_segment = generate_path_segment(Coordinate4D(1, 1, 1, 5))
    second_segment = generate_path_segment(Coordinate4D(4, 4, 4, 16))
    second_segment.index = 1
    stats = generate_allocation_statistics()
    return Allocation(agi, [first_segment, second_segment], stats)


def generate_space_allocation():
    agi = generate_space_agent()
    first_segment = generate_space_segment(Coordinate4D(3, 3, 3, 10))
    second_segment = generate_space_segment(Coordinate4D(40, 40, 40, 10))
    third_segment = generate_space_segment(Coordinate4D(10, 10, 10, 10))
    stats = generate_allocation_statistics()
    return Allocation(agi, [first_segment, second_segment, third_segment], stats)
