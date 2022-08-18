from AAS import ABCOwner


class FCFSABCOwner(ABCOwner):
    label = "FCFS A to B to C"
    description = "A owner with agents going from A to a number of stops"

    def __init__(self, name, color, stops, creation_ticks):
        super().__init__(name, color, stops, creation_ticks)
