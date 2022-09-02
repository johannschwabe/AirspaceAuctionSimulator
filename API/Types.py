from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field

class APIWorldCoordinates(BaseModel):
    long: float
    lat: float


class APIWeightedCoordinate(BaseModel):
    lat: float
    long: float
    value: float


class APISubselection(BaseModel):
    bottomLeft: Optional["APIWorldCoordinates"] = Field(None)
    topRight: Optional["APIWorldCoordinates"] = Field(None)


class APILocations(BaseModel):
    type: str
    points: List[APIWeightedCoordinate]


class APIOwner(BaseModel):
    color: str
    name: str
    agents: int
    minLocations: int
    maxLocations: int
    type: str
    classname: str
    allocator: str
    locations: List[APILocations]


class APIMap(BaseModel):
    coordinates: APIWorldCoordinates
    locationName: str
    neighbouringTiles: int
    bottomLeftCoordinate: APIWorldCoordinates
    topRightCoordinate: APIWorldCoordinates
    subselection: APISubselection
    resolution: int
    tiles: List[List[int]]
    height: int
    timesteps: int


class APIAvailableOwner(BaseModel):
    label: str
    classname: str
    description: str
    ownerType: str
    allocator: str
    minLocations: int
    maxLocations: int
    meta: List[object]


class APISimulationConfig(BaseModel):
    name: str
    description: str
    allocator: str
    map: APIMap
    owners: List[APIOwner]
    availableAllocators: Optional[List[str]]
    availableOwnersForAllocator: Optional[List[APIAvailableOwner]]
