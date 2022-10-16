import math
import random
from abc import ABC
from typing import Dict, List

from .WebBiddingStrategy import WebBiddingStrategy


class WebPathBiddingStrategy(WebBiddingStrategy, ABC):
    @staticmethod
    def meta() -> List[Dict]:
        return [
            {
                "key": "near_field",
                "label": "Near field size",
                "description": "Radius of reserved field",
                "type": "int",
                "value": math.ceil(random.random() * 3),
                "range": "1-3"
            },
            {
                "key": "battery",
                "label": "Battery capacity",
                "description": "Maximum flight time",
                "type": "int",
                "value": max(500, math.ceil(random.random() * 2000)),
                "range": "500-2000"
            },
            {
                "key": "speed",
                "label": "Ticks per voxel",
                "description": "Number ticks needed to traverse a voxel: 1 is the fastest",
                "type": "int",
                "value": math.ceil(random.random() * 3),
                "range": "1-3"
            },
        ]
