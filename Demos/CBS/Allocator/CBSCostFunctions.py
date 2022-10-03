from Demos.CBS.Allocator.CBSAllocatorHelpers import HighLevelNode


def path_length(node: "HighLevelNode"):
    return sum([sum([len(path.coordinates) for path in paths]) for paths in node.solution.values()])


def welfare(node: "HighLevelNode"):
    total_welfare = 0.0
    for agent in node.solution.keys():
        total_welfare += agent.value_for_segments(node.solution[agent])
    return -total_welfare  # nodes with lower welfare are investigated first, thus negative welfare
