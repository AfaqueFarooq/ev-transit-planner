from fastapi import APIRouter, Query, HTTPException
from app.services.vbb_service import vbb_service
from app.models.vbb_models import ReachableResponse

router = APIRouter()

@router.get("/", response_model=ReachableResponse)
async def get_reachable(
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location"),
    address: str = Query(..., description="Address of the location e.g. 10178 Berlin-Mitte, Münzstr. 12")
):
    try:
        data = await vbb_service.get_reachable(
            latitude=latitude,
            longitude=longitude,
            address=address
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))