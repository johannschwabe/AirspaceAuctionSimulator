import random
from time import time_ns

from API import APISimpleCoordinate
from Simulator import Environment
from Simulator.Agent import ABAgent
from Simulator.Coordinate import Coordinate4D
from Simulator.Generator.MapTile import MapTile
from Simulator.Owner import PathOwner, PathStop
from Simulator.AStar.AStar import AStar

dimensions = Coordinate4D(831, 30, 831, 20000)


def setup():
    random.seed(3)
    environment = Environment(dimensions, [], [MapTile(
        [15, 17161, 11475],
        dimensions,
        APISimpleCoordinate(lat=47.376034633497596, long=8.536376953124991),
        APISimpleCoordinate(lat=47.3685943521338, long=8.547363281249993)
    )])
    environment.init_blocker_tree()
    return environment


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


def writeCoords(env: Environment, filename: str):
    astar = AStar(env)
    f = open(filename, "w")
    agent = ABAgent(Coordinate4D.random(dimensions), Coordinate4D.random(dimensions))
    nr_tests = 20
    nr_success = 0
    start_t = time_ns()
    for _ in range(nr_tests):
        start = PathOwner.generate_stop_coordinate(PathStop("random"), env, 0, 1, 1)
        end = PathOwner.generate_stop_coordinate(PathStop("random"), env, 0, 1, 1)
        res, _ = astar.astar(start, end, agent)
        f.write(f"{start.x},{start.y},{start.z},{start.t}-{end.x},{end.y},{end.z},{end.t}-{len(res)}\n")
    f.close()


def test(env: Environment):
    astar = AStar(env)
    agent = ABAgent(Coordinate4D.random(dimensions), Coordinate4D.random(dimensions))
    nr_tests = 20
    nr_success = 0
    start_t = time_ns()
    segments = readCoords("optimal_paths.txt")
    sum_optimal_len = 0
    sum_achieved_len = 0
    for segment in segments:
        res, _ = astar.astar(segment["start"], segment["end"], agent)
        sum_achieved_len += len(res)
        sum_optimal_len += segment["optimal"]
        if len(res) != segment["optimal"]:
            print(f"Suboptimal Path found {len(res)} vs {segment['optimal']}")
        if len(res) > 0:
            nr_success += 1
    duration = (time_ns() - start_t) / 1e9
    print(
        f"Nr_tests: {nr_tests}, Duration: {duration:3f}s, Success: {nr_success}, {sum_achieved_len / sum_optimal_len}")


if __name__ == "__main__":
    envi = setup()
    test(envi)
