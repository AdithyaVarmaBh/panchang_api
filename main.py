from fastapi import FastAPI
from datetime import datetime
from astro_core import get_panchang_at_sunrise

app = FastAPI()

@app.post("/panchang")
def panchang_endpoint(payload: dict):
    dt = datetime.fromisoformat(payload["datetime_iso"])
    tz = payload["timezone"]
    lat = payload["latitude"]
    lon = payload["longitude"]
    return get_panchang_at_sunrise(dt, lat, lon, tz)