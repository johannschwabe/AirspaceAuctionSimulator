import math
import random


class PathBiddingStrategy:
    @staticmethod
    def meta():
        return [
            {
                "key": "near_field",
                "label": "Near field size",
                "description": "Radius of reserved field",
                "type": "int",
                "value": math.ceil(random.random() * 4),
                "range": "1-10"
            },
            {
                "key": "battery",
                "label": "Battery capacity",
                "description": "Maximum flight time",
                "type": "int",
                "value": math.ceil(random.random() * 1000),
                "range": "500-2000"
            },
            {
                "key": "speed",
                "label": "Ticks per voxel",
                "description": "Number ticks needed to traverse a voxel: 1 is the fastest",
                "type": "int",
                "value": math.ceil(random.random() * 5),
                "range": "1-10"
            },
        ]
