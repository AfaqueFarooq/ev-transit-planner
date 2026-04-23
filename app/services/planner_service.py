import asyncio
from app.services.chargetrip_service import chargetrip_service
from app.services.vbb_service import vbb_service


class PlannerService:

    async def plan_trip(
        self,
        vehicle_id: str,
        origin_lat: float,
        origin_lng: float,
        destination_lat: float,
        destination_lng: float,
        state_of_charge: int = 80
    ):
        # Step 1 — Create EV route on ChargeTrip
        route_id = await chargetrip_service.create_route(
            vehicle_id=vehicle_id,
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            destination_lat=destination_lat,
            destination_lng=destination_lng,
            state_of_charge=state_of_charge
        )

        # Step 2 — Poll until route calculation is done
        route = await self._wait_for_route(route_id)

        if not route or route.get("status") != "done":
            raise Exception("Route calculation failed or timed out")

        # Step 3 — Extract last charging stop before destination
        last_charging_stop = self._get_last_charging_stop(route)

        if not last_charging_stop:
            raise Exception("No charging stops found in route")

        # Step 4 — Swap coordinates [lng, lat] → lat, lng for VBB
        coordinates = last_charging_stop["geometry"]["coordinates"]
        lng = coordinates[0]
        lat = coordinates[1]
        station_name = last_charging_stop["properties"]["name"]

        #  TEMPORARILY
        print(f"Last charging stop: {station_name}")
        print(f"Coordinates: lat={lat}, lng={lng}")

        # Step 5 — Find nearest VBB transit stop
        nearby_stops = await vbb_service.get_nearby(
            latitude=lat,
            longitude=lng,
            results=5
        )

        if not nearby_stops:
            raise Exception("No transit stops found near charging station")

        nearest_stop = nearby_stops[0]
        nearest_stop_id = nearest_stop["id"]

        # Step 6 — Plan VBB journey to destination
        # Use Berlin Hauptbahnhof as default transit destination
        berlin_hbf_id = "900003201"
        journeys = await vbb_service.get_journeys(
            from_id=nearest_stop_id,
            to_id=berlin_hbf_id,
            results=2
        )

        # Step 7 — Return complete multimodal trip plan
        return {
            "ev_route": {
                "route_id": route_id,
                "status": route.get("status"),
                "charges": route["recommended"]["charges"],
                "total_distance_meters": route["recommended"]["distance"],
                "durations": route["recommended"]["durations"],
                "range_at_origin": route["recommended"]["range_at_origin"],
                "range_at_destination": route["recommended"]["range_at_destination"]
            },
            "last_charging_stop": {
                "name": station_name,
                "coordinates": {
                    "latitude": lat,
                    "longitude": lng
                }
            },
            "nearest_transit_stop": {
                "id": nearest_stop_id,
                "name": nearest_stop["name"],
                "distance_meters": nearest_stop.get("distance"),
                "products": nearest_stop.get("products")
            },
            "transit_journeys": journeys.get("journeys", [])
        }

    async def _wait_for_route(self, route_id: str, max_attempts: int = 10, delay: float = 2.0):
        """Poll getRoute until status is done or max attempts reached"""
        for attempt in range(max_attempts):
            route = await chargetrip_service.get_route(route_id)
            if route and route.get("status") == "done":
                return route
            await asyncio.sleep(delay)
        return None

    def _get_last_charging_stop(self, route: dict):
        """Extract the last charging stop before the final destination"""
        legs = route.get("recommended", {}).get("legs", [])
        # Find the last leg that is a charging station stop
        # The last leg is type "final" so we want the one before it
        for leg in reversed(legs):
            if leg.get("type") == "station":
                return leg.get("destination")
        return None


planner_service = PlannerService()