from typing import TYPE_CHECKING
from time import time_ns

from API import APISubselection
from API.WebClasses.Owners.WebPathOwner import WebPathOwner
from API.WebClasses.Owners.WebSpaceOwner import WebSpaceOwner
from Simulator.IO.Statistics import get_statistics_dict
from Simulator.IO.JSONS import JSONOwnerDescription, get_simulation_dict

if TYPE_CHECKING:
    from Simulator.Simulator import Simulator


def generate_output(simulator: 'Simulator', simulation_time: int, simulation_config):
    statistics_start_time = time_ns()
    statistics = get_statistics_dict(simulator)
    statistics_end_time = time_ns()
    statistics_duration = statistics_end_time - statistics_start_time

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
