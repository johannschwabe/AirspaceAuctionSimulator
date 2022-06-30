from enum import Enum


class Reason(Enum):
    FIRST_ALLOCATION = 1
    AGENT = 2
    BLOCKER = 3
    OWNER = 4
    NOT_IMPLEMENTED = 5
    ALLOCATION_FAILED = 6
