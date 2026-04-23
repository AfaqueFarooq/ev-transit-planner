from pydantic import BaseModel
from typing import Optional, List, Any


# --- Vehicle Models ---

class VehicleNaming(BaseModel):
    make: str
    model: str
    version: Optional[str] = None
    edition: Optional[str] = None


class VehicleBattery(BaseModel):
    usable_kwh: Optional[float] = None
    full_kwh: Optional[float] = None
    type: Optional[str] = None


class VehicleConnector(BaseModel):
    standard: Optional[str] = None
    max_electric_power: Optional[float] = None
    power: Optional[float] = None
    speed: Optional[float] = None


class VehicleDrivetrain(BaseModel):
    type: Optional[str] = None


class ChargetripRange(BaseModel):
    best: Optional[float] = None
    worst: Optional[float] = None


class VehicleRange(BaseModel):
    chargetrip_range: Optional[ChargetripRange] = None


class VehicleBody(BaseModel):
    seats: Optional[int] = None


class VehicleAvailability(BaseModel):
    status: Optional[str] = None


class Vehicle(BaseModel):
    id: str
    naming: VehicleNaming
    battery: Optional[VehicleBattery] = None
    connectors: Optional[List[VehicleConnector]] = None
    drivetrain: Optional[VehicleDrivetrain] = None
    range: Optional[VehicleRange] = None
    body: Optional[VehicleBody] = None
    availability: Optional[VehicleAvailability] = None


# --- Station Models ---

class StationLocation(BaseModel):
    type: Optional[str] = None
    coordinates: Optional[List[float]] = None


class ChargerStatus(BaseModel):
    free: Optional[int] = None
    busy: Optional[int] = None
    unknown: Optional[int] = None
    error: Optional[int] = None


class Charger(BaseModel):
    standard: Optional[str] = None
    power: Optional[float] = None
    status: Optional[ChargerStatus] = None


class StationAddress(BaseModel):
    city: Optional[str] = None
    street: Optional[str] = None
    country: Optional[str] = None


class StationOperator(BaseModel):
    name: Optional[str] = None


class Station(BaseModel):
    id: str
    name: Optional[str] = None
    location: Optional[StationLocation] = None
    physical_address: Optional[StationAddress] = None
    chargers: Optional[List[Charger]] = None
    status: Optional[str] = None
    operator: Optional[StationOperator] = None


# --- Route Models ---

class RouteGeometry(BaseModel):
    type: Optional[str] = None
    coordinates: Optional[List[float]] = None


class RouteProperties(BaseModel):
    name: Optional[str] = None
    station_id: Optional[str] = None


class RouteFeature(BaseModel):
    type: Optional[str] = None
    geometry: Optional[RouteGeometry] = None
    properties: Optional[RouteProperties] = None


class RouteDurations(BaseModel):
    total: Optional[int] = None
    charging: Optional[int] = None
    driving: Optional[int] = None


class RouteLeg(BaseModel):
    type: Optional[str] = None
    distance: Optional[float] = None
    origin: Optional[RouteFeature] = None
    destination: Optional[RouteFeature] = None
    range_at_origin: Optional[float] = None
    range_at_destination: Optional[float] = None
    range_after_charge: Optional[float] = None


class RouteRecommended(BaseModel):
    id: Optional[str] = None
    charges: Optional[int] = None
    distance: Optional[float] = None
    durations: Optional[RouteDurations] = None
    consumption: Optional[float] = None
    range_at_origin: Optional[float] = None
    range_at_destination: Optional[float] = None
    legs: Optional[List[RouteLeg]] = None


class Route(BaseModel):
    id: str
    status: Optional[str] = None
    recommended: Optional[RouteRecommended] = None


class CreateRouteResponse(BaseModel):
    route_id: str