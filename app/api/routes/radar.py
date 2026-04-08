from fastapi import APIRouter, Query, HTTPException
from app.services.vbb_service import vbb_service
from app.models.vbb_models import RadarResponse

router = APIRouter()

@router.get("/", response_model=RadarResponse)
async def get_radar(
    north: float = Query(..., description="North boundary of bounding box"),
    south: float = Query(..., description="South boundary of bounding box"),
    east: float = Query(..., description="East boundary of bounding box"),
    west: float = Query(..., description="West boundary of bounding box"),
    results: int = Query(5, description="Number of vehicles to return")
):
    try:
        data = await vbb_service.get_radar(
            north=north,
            south=south,
            east=east,
            west=west,
            results=results
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))