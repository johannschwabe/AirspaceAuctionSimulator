import math
import random


class SpaceBiddingStrategy:
    @staticmethod
    def meta():
        return [
            {
                "key": "size_x",
                "label": "Field Size X",
                "description": "Size of reserved field in X-Dimension",
                "type": "int",
                "value": math.ceil(random.random() * 100),
            },
            {
                "key": "size_y",
                "label": "Field Size Y",
                "description": "Size of reserved field in Y-Dimension",
                "type": "int",
                "value": math.ceil(random.random() * 100),
            },
            {
                "key": "size_z",
                "label": "Field Size Z",
                "description": "Size of reserved field in Z-Dimension",
                "type": "int",
                "value": math.ceil(random.random() * 100),
            },
            {
                "key": "size_t",
                "label": "Field Size T",
                "description": "Size of reserved field in T-Dimension",
                "type": "int",
                "value": math.ceil(random.random() * 100),
            },
        ]
