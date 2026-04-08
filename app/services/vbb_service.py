import httpx
from app.core.config import VBB_BASE_URL


class VBBService:

    def __init__(self):
        self.base_url = VBB_BASE_URL

    async def get_locations(self, query: str, results: int = 5):
        url = f"{self.base_url}/locations"
        params = {
            "query": query,
            "results": results,
            "poi": "false",
            "addresses": "false"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_departures(self, stop_id: str, results: int = 5):
        url = f"{self.base_url}/stops/{stop_id}/departures"
        params = {
            "results": results
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_journeys(self, from_id: str, to_id: str, results: int = 3):
        url = f"{self.base_url}/journeys"
        params = {
            "from": from_id,
            "to": to_id,
            "results": results
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_nearby(self, latitude: float, longitude: float, results: int = 5):
        url = f"{self.base_url}/locations/nearby"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "results": results
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_radar(self, north: float, south: float, east: float, west: float, results: int = 5):
        url = f"{self.base_url}/radar"
        params = {
            "north": north,
            "south": south,
            "east": east,
            "west": west,
            "results": results
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_reachable(self, latitude: float, longitude: float, address: str):
        url = f"{self.base_url}/stops/reachable-from"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "address": address
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()


vbb_service = VBBService()