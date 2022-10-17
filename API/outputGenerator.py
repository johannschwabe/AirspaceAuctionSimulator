from time import time_ns
from typing import TYPE_CHECKING

from API.WebClasses.Owners.WebPathOwner import WebPathOwner
from API.WebClasses.Owners.WebSpaceOwner import WebSpaceOwner
from Simulator.IO.JSONS import JSONOwnerDescription, get_simulation_dict
from Simulator.IO.Statistics import get_statistics_dict

if TYPE_CHECKING:
    from Simulator.Simulator import Simulator


def generate_output(simulator: 'Simulator', simulation_time: int, simulation_config):
    statistics_start_time = time_ns()
    statistics = get_statistics_dict(simulator)
    statistics_end_time = time_ns()
    statistics_duration = int((statistics_end_time - statistics_start_time) // 1e9)

    owner_map = {}
    for owner in simulator.owners:
        if isinstance(owner, WebSpaceOwner) or isinstance(owner, WebPathOwner):
            owner_map[owner.id] = JSONOwnerDescription(owner.color, owner.name).as_dict()
        else:
            owner_map[owner.id] = JSONOwnerDescription(owner.id,
                                                       hex(hash(owner.id) % 0xFFFFFF)[2:].zfill(6)).as_dict()

    return {
        "config": simulation_config,
        "owner_map": owner_map,
        "simulation": get_simulation_dict(simulator),
        "statistics": statistics,
        "statistics_compute_time": statistics_duration,
        "simulation_compute_time": simulation_time
    }
