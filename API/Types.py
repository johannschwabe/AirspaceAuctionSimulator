from typing import List, Optional, Dict, Any

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


class APIBiddingStrategy(BaseModel):
    minLocations: int
    maxLocations: int
    allocationType: str
    classname: str
    meta: List[Dict[str, Any]]


class APIOwner(BaseModel):
    color: str
    name: str
    agents: int
    biddingStrategy: APIBiddingStrategy
    locations: List[APILocations]
    valueFunction: str


class APIMap(BaseModel):
    coordinates: APIWorldCoordinates
    locationName: str
    neighbouringTiles: int
    subselection: Optional[APISubselection]
    resolution: int
    height: int
    timesteps: int
    bottomLeftCoordinate: Optional[APIWorldCoordinates]
    topRightCoordinate: Optional[APIWorldCoordinates]
    tiles: Optional[List[List[int]]]
    minHeight: int
    allocationPeriod: int


class APISimulationConfig(BaseModel):
    name: str
    description: str
    allocator: str
    map: APIMap
    owners: List[APIOwner]
    paymentRule: str
