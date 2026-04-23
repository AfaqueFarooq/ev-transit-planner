from pydantic import BaseModel
from typing import Optional, List, Any


# --- EV Route Models ---

class RouteDurations(BaseModel):
    total: Optional[int] = None
    charging: Optional[int] = None
    driving: Optional[int] = None


class EVRoute(BaseModel):
    route_id: str
    status: Optional[str] = None
    charges: Optional[int] = None
    total_distance_meters: Optional[float] = None
    durations: Optional[RouteDurations] = None
    range_at_origin: Optional[float] = None
    range_at_destination: Optional[float] = None


# --- Charging Stop Models ---

class Coordinates(BaseModel):
    latitude: float
    longitude: float


class LastChargingStop(BaseModel):
    name: Optional[str] = None
    coordinates: Optional[Coordinates] = None


# --- Transit Stop Models ---

class Products(BaseModel):
    suburban: bool
    subway: bool
    tram: bool
    bus: bool
    ferry: bool
    express: bool
    regional: bool


class NearestTransitStop(BaseModel):
    id: str
    name: str
    distance_meters: Optional[int] = None
    products: Optional[Products] = None


# --- Complete Trip Plan Model ---

class TripPlan(BaseModel):
    ev_route: EVRoute
    last_charging_stop: LastChargingStop
    nearest_transit_stop: NearestTransitStop
    transit_journeys: List[Any] = []