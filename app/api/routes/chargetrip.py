from fastapi import APIRouter, HTTPException, Query
from app.services.chargetrip_service import ChargetripService  

router = APIRouter()

@router.get("/vehicles")
async def get_vehicles(
    size: int = Query(10, description="Number of vehicles to retrieve")):
    try:
        data = await ChargetripService().get_vehicle_list(size=size)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/stations")
async def get_stations(
    latitude: float = Query(..., description="Latitude of location"),
    longitude: float = Query(..., description="Longitude of location"),
    distance: int = Query(5000, description="Search radius in meters max 10000")
):
    try:
        data = await ChargetripService().get_stations_around(
            latitude=latitude,
            longitude=longitude,
            distance=distance
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/routes")
async def create_route(
    vehicle_id: str = Query(..., description="ChargeTrip vehicle ID"),
    origin_lat: float = Query(..., description="Origin latitude"),
    origin_lng: float = Query(..., description="Origin longitude"),
    destination_lat: float = Query(..., description="Destination latitude"),
    destination_lng: float = Query(..., description="Destination longitude"),
    state_of_charge: int = Query(80, description="Battery percentage at start")
):
    try:
        route_id = await ChargetripService().create_route(
            vehicle_id=vehicle_id,
            origin_lng=origin_lng,
            origin_lat=origin_lat,
            destination_lng=destination_lng,
            destination_lat=destination_lat,
            state_of_charge=state_of_charge
        )
        return {"route_id": route_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/routes/{route_id}")
async def get_route(route_id: str):
    try:
        data = await ChargetripService().get_route(route_id=route_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
