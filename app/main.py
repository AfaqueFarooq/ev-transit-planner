from fastapi import FastAPI
from app.core.config import APP_NAME, DEBUG
from app.api.routes import locations, departures, journeys, radar, reachable , chargetrip

app = FastAPI(
    title=APP_NAME,
    description="A multimodal trip planner combining VBB public transport and EV charging data.",
    version="1.0.0",
    debug=DEBUG
)

# VBB routes
app.include_router(locations.router, prefix="/api/locations", tags=["Locations"])
app.include_router(departures.router, prefix="/api/departures", tags=["Departures"])
app.include_router(journeys.router, prefix="/api/journeys", tags=["Journeys"])
app.include_router(radar.router, prefix="/api/radar", tags=["Radar"])
app.include_router(reachable.router, prefix="/api/reachable", tags=["Reachable"])

# ChargeTrip routes
app.include_router(chargetrip.router, prefix="/api/chargetrip", tags=["ChargeTrip"])


@app.get("/", tags=["Health"])
def root():
    return {
        "app": APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }