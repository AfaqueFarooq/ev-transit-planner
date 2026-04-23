from fastapi import APIRouter, Query, HTTPException
from app.services.vbb_service import vbb_service
from app.models.vbb_models import JourneysResponse

router = APIRouter()

@router.get("/", response_model=JourneysResponse)
async def get_journeys(
    from_id: str = Query(..., description="Origin stop ID"),
    to_id: str = Query(..., description="Destination stop ID"),
    results: int = Query(3, description="Number of journeys to return")
):
    try:
        data = await vbb_service.get_journeys(
            from_id=from_id,
            to_id=to_id,
            results=results
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))