import math
import random
from time import time_ns

from API import APIWorldCoordinates, Area, EnvironmentGen, MapTile
from Demos.FCFS import FCFSBidTracker, FCFSPathBiddingStrategy, FCFSPathValueFunction
from Simulator import AStar, Coordinate4D, Environment, GridLocation, GridLocationType, PathAgent, PathOwner

map_height = 30
time_steps = 20000


def setup():
    random.seed(0)
    area = Area(APIWorldCoordinates(lat=47.3685943521338, long=8.536376953124991),
                APIWorldCoordinates(lat=47.376034633497596, long=8.547363281249993),
                2)
    size = area.dimension
    dimensions = Coordinate4D(math.floor(size[0]),
                              math.floor(map_height / area.resolution),
                              math.floor(size[1]),
                              time_steps)
    print(dimensions)
    environment = EnvironmentGen(dimensions, [MapTile([15, 17161, 11475], area)], area).generate()
    return environment


def read_coords(filename: str):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    res = []
    for line in lines:
        parts = line.split("-")
        start_parts = parts[0].split(",")
        start = Coordinate4D(int(start_parts[0]), int(start_parts[1]), int(start_parts[2]), int(start_parts[3]))
        start_parts = parts[1].split(",")
        end = Coordinate4D(int(start_parts[0]), int(start_parts[1]), int(start_parts[2]), int(start_parts[3]))
        segment = {"start": start, "end": end, "optimal": int(parts[2])}
        res.append(segment)
    return res


def write_coords(environment: Environment, filename: str):
    astar = AStar(environment, FCFSBidTracker(), max_iter=-1, g_sum=1., height_adjust=0.)
    f = open(filename, "w")
    nr_tests = 20
    for index in range(nr_tests):
        print(f"Test {index}")
        start = PathOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)),
                                                   environment, 0, 1)
        end = PathOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)),
                                                 environment,
                                                 0, 1)
        agent = PathAgent("agent-id", FCFSPathBiddingStrategy(), FCFSPathValueFunction(), [start, end], [])
        res, _ = astar.astar(start, end, agent)
        f.write(f"{start.x},{start.y},{start.z},{start.t}-{end.x},{end.y},{end.z},{end.t}-{len(res)}\n")
    f.close()


def test_coords(environment: Environment, g_sum, height_adjust):
    astar = AStar(environment, FCFSBidTracker(), max_iter=-1, g_sum=g_sum, height_adjust=height_adjust)
    nr_tests = 20
    nr_success = 0
    start_t = time_ns()
    segments = read_coords("Development/optimal_paths.txt")
    sum_optimal_len = 0
    sum_achieved_len = 0

    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        agent = PathAgent("agent-id", FCFSPathBiddingStrategy(), FCFSPathValueFunction(), [start, end], [])
        res, _ = astar.astar(segment["start"], segment["end"], agent)
        if len(res) > 0:
            nr_success += 1
            sum_achieved_len += len(res)
            sum_optimal_len += segment["optimal"]

    duration = time_ns() - start_t
    print(
        f"Nr_tests: {nr_tests}, Duration: {duration / 1e9:3f}s, Success: {nr_success}, "
        f"Optimality: {sum_optimal_len / sum_achieved_len} "
    )


def write():
    environment = setup()
    write_coords(environment, "optimal_paths.txt")


def test():
    environment = setup()
    print("BASE")
    test_coords(environment, 0.1, 0.05)
    print()
    print("VARIANT: g-sum: 0.05")
    test_coords(environment, 0.05, 0.05)
    print()
    print("VARIANT: g-sum: 0.2")
    test_coords(environment, 0.2, 0.05)
    print()
    print("VARIANT: height-adjust: 0.")
    test_coords(environment, 0.1, 0.)
    print()
    print("VARIANT: height-adjust: 0.1")
    test_coords(environment, 0.1, 0.1)
    print()
    print("VARIANT: height-adjust: 0.01")
    test_coords(environment, 0.1, 0.01)


if __name__ == "__main__":
    write()
