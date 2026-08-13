from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pytz

from astro_core import to_julian_day, get_tithi, get_nakshatra

app = FastAPI()


class PanchangRequest(BaseModel):
    datetime_iso: str
    timezone: str
    latitude: float
    longitude: float


@app.post("/panchang")
def panchang(req: PanchangRequest):
    tz = pytz.timezone(req.timezone)
    naive_dt = datetime.fromisoformat(req.datetime_iso)
    dt = tz.localize(naive_dt)

    jd = to_julian_day(dt)

    tithi = get_tithi(jd)
    nakshatra = get_nakshatra(jd)

    return {
        "datetime": dt.isoformat(),
        "timezone": req.timezone,
        "latitude": req.latitude,
        "longitude": req.longitude,
        "tithi": tithi,
        "nakshatra": nakshatra
    }
