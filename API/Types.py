from typing import List, Optional, Dict, Any

from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(extra="ignore")

    minLocations: int
    maxLocations: int
    allocationType: str
    classname: str
    meta: List[Dict[str, Any]]


class APIOwner(BaseModel):
    color: str
    name: str
    agents: int = Field(ge=1, le=50)
    biddingStrategy: APIBiddingStrategy
    locations: List[APILocations]
    valueFunction: str


class APIMap(BaseModel):
    coordinates: APIWorldCoordinates
    locationName: str
    neighbouringTiles: int = Field(ge=0, le=3)
    subselection: Optional[APISubselection] = None
    resolution: int = Field(ge=1, le=50)
    height: int = Field(ge=1, le=200)
    timesteps: int = Field(ge=1, le=500)
    bottomLeftCoordinate: Optional[APIWorldCoordinates] = None
    topRightCoordinate: Optional[APIWorldCoordinates] = None
    tiles: Optional[List[List[int]]] = None
    minHeight: int = Field(ge=0, le=100)
    allocationPeriod: int = Field(ge=1, le=100)


class APISimulationConfig(BaseModel):
    name: str
    description: str
    allocator: str
    map: APIMap
    owners: List[APIOwner] = Field(min_length=1, max_length=20)
    paymentRule: str
