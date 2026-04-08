from fastapi import APIRouter, Query, HTTPException
from app.services.vbb_service import vbb_service

router = APIRouter()

@router.get("/search")
async def search_locations(
    query: str = Query(..., description="Stop name to search for"),
    results: int = Query(5, description="Number of results to return")
):
    try:
        data = await vbb_service.get_locations(query=query, results=results)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/nearby")
async def get_nearby(
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location"),
    results: int = Query(5, description="Number of nearby stops to return")
):
    try:
        data = await vbb_service.get_nearby(
            latitude=latitude,
            longitude=longitude,
            results=results
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))