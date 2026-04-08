from pydantic import BaseModel
from typing import Optional, List


# --- Location Models ---

class Location(BaseModel):
    type: str
    id: Optional[str] = None
    latitude: float
    longitude: float


class Products(BaseModel):
    suburban: bool
    subway: bool
    tram: bool
    bus: bool
    ferry: bool
    express: bool
    regional: bool


class Stop(BaseModel):
    type: str
    id: str
    name: str
    location: Location
    products: Products


# --- Departure Models ---

class Line(BaseModel):
    type: str
    id: Optional[str] = None
    name: str
    mode: str
    product: str


class Departure(BaseModel):
    tripId: str
    stop: Stop
    when: Optional[str] = None
    plannedWhen: Optional[str] = None
    delay: Optional[int] = None
    platform: Optional[str] = None
    plannedPlatform: Optional[str] = None
    direction: Optional[str] = None
    cancelled: Optional[bool] = None
    line: Line


class DeparturesResponse(BaseModel):
    departures: List[Departure]


# --- Journey Models ---

class Leg(BaseModel):
    origin: Optional[Stop] = None
    destination: Optional[Stop] = None
    departure: Optional[str] = None
    plannedDeparture: Optional[str] = None
    departureDelay: Optional[int] = None
    arrival: Optional[str] = None
    plannedArrival: Optional[str] = None
    arrivalDelay: Optional[int] = None
    reachable: Optional[bool] = None
    walking: Optional[bool] = None
    distance: Optional[int] = None
    line: Optional[Line] = None


class Journey(BaseModel):
    type: str
    legs: List[Leg]


class JourneysResponse(BaseModel):
    journeys: List[Journey]


# --- Nearby Models ---

class NearbyStop(BaseModel):
    type: str
    id: str
    name: str
    location: Location
    products: Products
    distance: Optional[int] = None


# --- Radar Models ---

class RadarMovement(BaseModel):
    tripId: str
    direction: Optional[str] = None
    line: Line
    location: Location


class RadarResponse(BaseModel):
    movements: List[RadarMovement]


# --- Reachable Models ---

class ReachableGroup(BaseModel):
    duration: int
    stations: List[Stop]


class ReachableResponse(BaseModel):
    reachable: List[ReachableGroup]