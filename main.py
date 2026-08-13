from fastapi import FastAPI
from datetime import datetime
from astro_core import get_panchang_at_sunrise, to_julian_day, get_tithi, get_nakshatra

app = FastAPI()

@app.post("/panchang_sunrise")
def panchang_sunrise_endpoint(payload: dict):
    dt = datetime.fromisoformat(payload["datetime_iso"])
    tz = payload["timezone"]
    lat = payload["latitude"]
    lon = payload["longitude"]
    return get_panchang_at_sunrise(dt, lat, lon, tz)

@app.post("/panchang_time")
def panchang_time_endpoint(payload: dict):
    dt = datetime.fromisoformat(payload["datetime_iso"])
    tz = payload["timezone"]
    lat = payload["latitude"]
    lon = payload["longitude"]

    jd = to_julian_day(dt)
    tithi = get_tithi(jd)
    nakshatra = get_nakshatra(jd)

    return {
        "datetime": dt.isoformat(),
        "tithi": tithi,
        "nakshatra": nakshatra
    }