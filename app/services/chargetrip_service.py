import httpx
from app.core.config import CHARGETRIP_URL, CHARGETRIP_CLIENT_ID, CHARGETRIP_APP_ID

class ChargetripService:
    def __init__(self):
        self.url = CHARGETRIP_URL
        self.headers = {
            "x-client-id": CHARGETRIP_CLIENT_ID,
            "x-app-id": CHARGETRIP_APP_ID,
            "Content-Type": "application/json"
        }

    async def _query(self, query: str, variables: dict = None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        
    async def get_vehicle_list(self, size: int = 10):
            query = """
            {
            vehicleList(size: %d) {
                id
                naming {
                make
                model
                version
                edition
                }
                battery {
                usable_kwh
                full_kwh
                type
                }
                connectors {
                standard
                max_electric_power
                power
                speed
                }
                drivetrain {
                type
                }
                range {
                chargetrip_range {
                    best
                    worst
                }
                }
                body {
                seats
                }
                availability {
                status
                }
            }
            }
            """ % size
            data = await self._query(query)
            return data["data"]["vehicleList"]
    
    async def get_stations_around(self, latitude: float, longitude: float, distance: int = 5000):
            query = """
            {
            stationAround(
                filter: {
                location: { type: Point, coordinates: [%f, %f] }
                distance: %d
                }
                size: 10
                page: 0
            ) {
                id
                name
                location {
                type
                coordinates
                }
                physical_address {
                city
                street
                country
                }
                chargers {
                standard
                power
                status {
                    free
                    busy
                    unknown
                    error
                }
                }
                status
                operator {
                name
                }
            }
            }
            """ % (longitude, latitude, distance)
            data = await self._query(query)
            return data["data"]["stationAround"]
    
    async def create_route(self, vehicle_id: str, origin_lng: float, origin_lat: float,
                            destination_lng: float, destination_lat: float,
                            state_of_charge: int = 80):
            query = """
            mutation createRoute($vehicleId: ID!) {
            createRoute(
                input: {
                vehicle: {
                    id: $vehicleId
                    battery: { state_of_charge: { value: %d, type: percentage } }
                    climate: true
                }
                origin: {
                    type: Feature
                    properties: { location: { name: "Origin" } vehicle: { occupants: 1 } }
                    geometry: { type: Point, coordinates: [%f, %f] }
                }
                destination: {
                    type: Feature
                    properties: { location: { name: "Destination" } }
                    geometry: { type: Point, coordinates: [%f, %f] }
                }
                }
            )
            }
            """ % (state_of_charge, origin_lng, origin_lat, destination_lng, destination_lat)
            variables = {"vehicleId": vehicle_id}
            data = await self._query(query, variables)
            return data["data"]["createRoute"]
    
    async def get_route(self, route_id: str):
            query = """
            {
            getRoute(id: "%s") {
                id
                status
                recommended {
                id
                charges
                distance(unit: meter)
                durations {
                    total
                    charging
                    driving
                }
                consumption
                range_at_origin
                range_at_destination
                legs {
                    type
                    distance(unit: meter)
                    origin {
                    geometry {
                        coordinates
                    }
                    properties {
                        name
                        station_id
                    }
                    }
                    destination {
                    geometry {
                        coordinates
                    }
                    properties {
                        name
                        station_id
                    }
                    }
                    range_at_origin
                    range_at_destination
                    range_after_charge
                }
                }
            }
            }
            """ % route_id
            data = await self._query(query)
            return data["data"]["getRoute"]
    
chargetrip_service = ChargetripService()

