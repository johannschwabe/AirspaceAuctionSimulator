from abc import ABC, abstractmethod

from Demos.CBS.Allocator.CBSAllocatorHelpers import HighLevelNode


class CostFunction(ABC):
    failed_allocation_valid = False

    @staticmethod
    @abstractmethod
    def __call__(node: "HighLevelNode"):
        pass


class PathLength(CostFunction):
    failed_allocation_valid = False

    @staticmethod
    def __call__(node: "HighLevelNode"):
        return sum([sum([len(path.coordinates) for path in paths]) for paths in node.solution.values()])


class Welfare(CostFunction):
    failed_allocation_valid = True

    @staticmethod
    def __call__(node: "HighLevelNode"):
        total_welfare = 0.0
        for agent in node.solution.keys():
            total_welfare += agent.value_for_segments(node.solution[agent])
        return -total_welfare  # nodes with lower welfare are investigated first, thus negative welfare
