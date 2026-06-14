from fastapi import FastAPI
from app.api.routes.chargetrip import chargetrip
from app.api.routes.vbb import departures, journeys, locations, radar
from app.core.config import APP_NAME, DEBUG
from app.api.routes.vbb import reachable
from app.api.routes.planner import trip
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


app = FastAPI(
    title=APP_NAME,
    description="A multimodal trip planner combining VBB public transport and EV charging data.",
    version="1.0.0",
    debug=DEBUG
)

# VBB routes
app.include_router(locations.router, prefix="/api/v1/locations", tags=["Locations"])
app.include_router(departures.router, prefix="/api/v1/departures", tags=["Departures"])
app.include_router(journeys.router, prefix="/api/v1/journeys", tags=["Journeys"])
app.include_router(radar.router, prefix="/api/v1/radar", tags=["Radar"])
app.include_router(reachable.router, prefix="/api/v1/reachable", tags=["Reachable"])

# ChargeTrip routes
app.include_router(chargetrip.router, prefix="/api/v1/chargetrip", tags=["ChargeTrip"])

app.include_router(trip.router, prefix="/api/v1/planner", tags=["Trip Planner"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", tags=["Health"])
def root():
    return {
        "app": APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/ui")
def ui():
    return FileResponse("app/static/index.html")