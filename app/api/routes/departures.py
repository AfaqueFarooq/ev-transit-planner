from fastapi import APIRouter, Query, HTTPException
from app.services.vbb_service import vbb_service

router = APIRouter()

@router.get("/{stop_id}")
async def get_departures(
    stop_id: str,
    results: int = Query(5, description="Number of departures to return")
):
    try:
        data = await vbb_service.get_departures(stop_id=stop_id, results=results)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))