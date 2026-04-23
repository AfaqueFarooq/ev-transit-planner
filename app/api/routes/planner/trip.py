from fastapi import APIRouter, Query, HTTPException
from app.services.planner_service import planner_service
from app.models.planner_models import TripPlan

router = APIRouter()


@router.get("/trip", response_model=TripPlan)
async def plan_trip(
    vehicle_id: str = Query(..., description="ChargeTrip vehicle ID"),
    origin_lat: float = Query(..., description="Origin latitude"),
    origin_lng: float = Query(..., description="Origin longitude"),
    destination_lat: float = Query(..., description="Destination latitude"),
    destination_lng: float = Query(..., description="Destination longitude"),
    state_of_charge: int = Query(80, description="Battery percentage at start")
):
    try:
        result = await planner_service.plan_trip(
            vehicle_id=vehicle_id,
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            destination_lat=destination_lat,
            destination_lng=destination_lng,
            state_of_charge=state_of_charge
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))