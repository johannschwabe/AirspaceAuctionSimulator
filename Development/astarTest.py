import random
from time import time_ns

from API.API import APISimpleCoordinates
from API.Generator.EnvironmentGen import EnvironmentGen
from API.Generator.MapTile import MapTile
from Demos.FCFS.Agents.FCFSABAgent import FCFSABAgent
from Demos.FCFS.Allocator.FCFSAllocator import FCFSAllocator
from Simulator import AStar, Coordinate4D, ABOwner, GridLocation, GridLocationType, Simulator

dimensions = Coordinate4D(831, 30, 831, 20000)


def setup():
    random.seed(0)
    environment = EnvironmentGen(dimensions, [MapTile(
        [15, 17161, 11475],
        dimensions,
        APISimpleCoordinates(lat=47.376034633497596, long=8.536376953124991),
        APISimpleCoordinates(lat=47.3685943521338, long=8.547363281249993)
    )]).generate()
    allocator = FCFSAllocator()
    simulator = Simulator([], allocator, environment)
    return simulator


def readCoords(filename: str):
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


def writeCoords(simulator: Simulator, filename: str):
    astar = AStar(simulator.environment)
    f = open(filename, "w")
    nr_tests = 20
    for index in range(nr_tests):
        print(f"Test {index}")
        start = ABOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)),
                                                 simulator.environment, 0, 1, 1)
        end = ABOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)), simulator.environment,
                                               0, 1, 1)
        agent = FCFSABAgent(start, end, simulator)
        res, _ = astar.astar(start, end, agent)
        f.write(f"{start.x},{start.y},{start.z},{start.t}-{end.x},{end.y},{end.z},{end.t}-{len(res)}\n")
    f.close()


def testCoords(simulator: Simulator, g_sum, height_adjust):
    astar = AStar(simulator.environment, max_iter=1_000_000, g_sum=g_sum, height_adjust=height_adjust)
    nr_tests = 20
    nr_success = 0
    start_t = time_ns()
    segments = readCoords("optimal_paths.txt")
    sum_optimal_len = 0
    sum_achieved_len = 0

    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        agent = FCFSABAgent(start, end, simulator)
        res, _ = astar.astar(segment["start"], segment["end"], agent)
        if len(res) > 0:
            nr_success += 1
            sum_achieved_len += len(res)
            sum_optimal_len += segment["optimal"]

    duration = time_ns() - start_t
    print(
        f"Nr_tests: {nr_tests}, Duration: {duration:3f}s, Success: {nr_success}, {sum_achieved_len / sum_optimal_len}"
    )


def write():
    simulator = setup()
    writeCoords(simulator, "Development/optimal_paths.txt")


def test():
    simulator = setup()
    print("g sum: 0.1")
    testCoords(simulator, 0.1, False)
    print()
    print("g sum: 0.2")
    testCoords(simulator, 0.2, False)
    print()
    print("g sum: 0.3")
    testCoords(simulator, 0.3, False)
    print()
    print("height adjust")
    testCoords(simulator, 0.2, True)


if __name__ == "__main__":
    write()
