from time import tzname

import swisseph as swe
from datetime import datetime
import pytz
# from astral import LocationInfo
# from astral.sun import sun

swe.set_ephe_path('.')
swe.set_sid_mode(swe.SIDM_LAHIRI,0,0)


def normalize_angle(angle: float) -> float:
    return angle % 360.0


def to_julian_day(dt: datetime) -> float:
    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    )

def get_true_sunrise(date: datetime, lat: float, lon: float, tz: str) -> datetime:
    tzinfo = pytz.timezone(tz)

    jd = to_julian_day(date)

    rs = swe.rise_trans(
        jd,
        swe.SUN,
        lon,
        lat,
        rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER
    )

    sunrise_jd = rs[1]

    sunrise_utc = swe.revjul(sunrise_jd, swe.SE_GREG_CAL)
    sunrise_dt = datetime(
        sunrise_utc[0],
        sunrise_utc[1],
        sunrise_utc[2],
        int(sunrise_utc[3]),
        int((sunrise_utc[3] % 1) * 60),
        int((((sunrise_utc[3] % 1) * 60) % 1) * 60),
        tzinfo=pytz.utc
    )

    return sunrise_dt.astimezone(tzinfo)

def get_sun_longitude(jd: float) -> float:
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    result = swe.calc(jd, swe.SUN, flags )
    lon = result[0][0]
    return normalize_angle(lon)


def get_moon_longitude(jd: float) -> float:
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    result = swe.calc(jd, swe.MOON, flags)
    lon = result[0][0]
    return normalize_angle(lon)

# def get_sunrise(date: datetime, lat: float, lon: float, tz: str) -> datetime:
# 	"""
# 	Sunrise using Astral (robust on macOS)
# 	"""
# 	tzinfo = pytz.timezone(tz)
#
# 	loc = LocationInfo(
# 		name = "Custom",
# 		region = "Custom",
# 		timezone = tz,
# 		latitude = lat,
# 		longitude = lon
# 	)
#
# 	s=sun(loc.observer, date=date, tzinfo=tzinfo)
# 	return s["sunrise"]

def get_tithi(jd: float) -> dict:
    sun_lon = get_sun_longitude(jd)
    moon_lon = get_moon_longitude(jd)

    diff = normalize_angle(moon_lon - sun_lon)

    tithi_index = int(diff // 12)
    tithi_num = tithi_index + 1

    paksha = "Shukla" if tithi_num <= 15 else "Krishna"

    tithi_names = [
        "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashti", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
        "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashti", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
    ]

    return {
        "tithi_number": tithi_num,
        "tithi_name": tithi_names[tithi_index],
        "paksha": paksha
    }


def get_nakshatra(jd: float) -> dict:
    moon_lon = get_moon_longitude(jd)

    # Each nakshatra = 13°20' = 13.333333 degrees
    nak_index = int(moon_lon // 13.333333333333)

    nak_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
        "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
        "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
        "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashada",
        "Uttara Ashada", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]

    return {
        "nakshatra_index": nak_index + 1,
        "nakshatra_name": nak_names[nak_index]
    }

def get_panchang_at_sunrise(date: datetime, lat: float, lon: float, tz: str) -> dict:
	sunrise = get_true_sunrise(date, lat, lon, tz)

	jd_sunrise = to_julian_day(sunrise)

	tithi = get_tithi(jd_sunrise)
	nakshatra = get_nakshatra(jd_sunrise)

	return {
		"sunrise": sunrise.isoformat(),
		"tithi": tithi,
		"nakshatra": nakshatra
	}

def get_panchang_at_time(dt: datetime) -> dict:
    jd = to_julian_day(dt)
    tithi = get_tithi(jd)
    nakshatra = get_nakshatra(jd)

    return {
        "datetime": dt.isoformat(),
        "tithi": tithi,
        "nakshatra": nakshatra
    }