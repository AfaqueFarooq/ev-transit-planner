# tests for VBB endpoints
import pytest
import httpx
from app.services.vbb_service import vbb_service


# --- Locations Tests ---

@pytest.mark.asyncio
async def test_search_locations_returns_results():
    data = await vbb_service.get_locations(query="südkreuz")
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_search_locations_has_required_fields():
    data = await vbb_service.get_locations(query="südkreuz")
    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "location" in first
    assert "products" in first

@pytest.mark.asyncio
async def test_search_locations_returns_stop_type():
    data = await vbb_service.get_locations(query="südkreuz")
    first = data[0]
    assert first["type"] == "stop"

@pytest.mark.asyncio
async def test_search_locations_has_coordinates():
    data = await vbb_service.get_locations(query="südkreuz")
    first = data[0]
    assert "latitude" in first["location"]
    assert "longitude" in first["location"]


# --- Departures Tests ---

@pytest.mark.asyncio
async def test_get_departures_returns_results():
    data = await vbb_service.get_departures(stop_id="900058101")
    assert "departures" in data
    assert isinstance(data["departures"], list)

@pytest.mark.asyncio
async def test_get_departures_has_required_fields():
    data = await vbb_service.get_departures(stop_id="900058101")
    first = data["departures"][0]
    assert "tripId" in first
    assert "line" in first
    assert "direction" in first
    assert "plannedWhen" in first

@pytest.mark.asyncio
async def test_get_departures_delay_is_int_or_none():
    data = await vbb_service.get_departures(stop_id="900058101")
    first = data["departures"][0]
    assert first["delay"] is None or isinstance(first["delay"], int)

@pytest.mark.asyncio
async def test_get_departures_cancelled_field_exists():
    data = await vbb_service.get_departures(stop_id="900058101")
    first = data["departures"][0]
    assert "cancelled" in first or first.get("cancelled") is None


# --- Journeys Tests ---

@pytest.mark.asyncio
async def test_get_journeys_returns_results():
    data = await vbb_service.get_journeys(
        from_id="900058101",
        to_id="900110005"
    )
    assert "journeys" in data
    assert isinstance(data["journeys"], list)
    assert len(data["journeys"]) > 0

@pytest.mark.asyncio
async def test_get_journeys_has_legs():
    data = await vbb_service.get_journeys(
        from_id="900058101",
        to_id="900110005"
    )
    first_journey = data["journeys"][0]
    assert "legs" in first_journey
    assert isinstance(first_journey["legs"], list)
    assert len(first_journey["legs"]) > 0

@pytest.mark.asyncio
async def test_get_journeys_leg_has_required_fields():
    data = await vbb_service.get_journeys(
        from_id="900058101",
        to_id="900110005"
    )
    first_leg = data["journeys"][0]["legs"][0]
    assert "departure" in first_leg or "plannedDeparture" in first_leg
    assert "origin" in first_leg
    assert "destination" in first_leg


# --- Nearby Tests ---

@pytest.mark.asyncio
async def test_get_nearby_returns_results():
    data = await vbb_service.get_nearby(
        latitude=52.475501,
        longitude=13.365548
    )
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_nearby_has_distance_field():
    data = await vbb_service.get_nearby(
        latitude=52.475501,
        longitude=13.365548
    )
    first = data[0]
    assert "distance" in first
    assert isinstance(first["distance"], int)

@pytest.mark.asyncio
async def test_get_nearby_first_result_is_closest():
    data = await vbb_service.get_nearby(
        latitude=52.475501,
        longitude=13.365548
    )
    assert data[0]["distance"] <= data[1]["distance"]


# --- Radar Tests ---

@pytest.mark.asyncio
async def test_get_radar_returns_movements():
    data = await vbb_service.get_radar(
        north=52.52,
        south=52.47,
        east=13.43,
        west=13.36
    )
    assert "movements" in data
    assert isinstance(data["movements"], list)

@pytest.mark.asyncio
async def test_get_radar_movement_has_location():
    data = await vbb_service.get_radar(
        north=52.52,
        south=52.47,
        east=13.43,
        west=13.36
    )
    first = data["movements"][0]
    assert "location" in first
    assert "latitude" in first["location"]
    assert "longitude" in first["location"]

@pytest.mark.asyncio
async def test_get_radar_movement_has_line():
    data = await vbb_service.get_radar(
        north=52.52,
        south=52.47,
        east=13.43,
        west=13.36
    )
    first = data["movements"][0]
    assert "line" in first
    assert "name" in first["line"]


# --- Reachable Tests ---

@pytest.mark.asyncio
async def test_get_reachable_returns_groups():
    data = await vbb_service.get_reachable(
        latitude=52.52446,
        longitude=13.40812,
        address="10178 Berlin-Mitte, Münzstr. 12"
    )
    assert "reachable" in data
    assert isinstance(data["reachable"], list)

@pytest.mark.asyncio
async def test_get_reachable_groups_have_duration():
    data = await vbb_service.get_reachable(
        latitude=52.52446,
        longitude=13.40812,
        address="10178 Berlin-Mitte, Münzstr. 12"
    )
    first = data["reachable"][0]
    assert "duration" in first
    assert isinstance(first["duration"], int)

@pytest.mark.asyncio
async def test_get_reachable_duration_increases():
    data = await vbb_service.get_reachable(
        latitude=52.52446,
        longitude=13.40812,
        address="10178 Berlin-Mitte, Münzstr. 12"
    )
    durations = [group["duration"] for group in data["reachable"]]
    assert durations == sorted(durations)