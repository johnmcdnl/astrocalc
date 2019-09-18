import datetime
import math
import sys
from datetime import datetime, timedelta, date

import pytz as pytz
from pytz.reference import Local


def sin(n):
    return math.sin(math.radians(n))


def cos(n):
    return math.cos(math.radians(n))


def tan(n):
    return math.tan(math.radians(n))


def asin(n):
    return math.degrees(math.asin(n))


def acos(n):
    return math.degrees(math.acos(n))


def atan(n):
    return math.degrees(math.atan(n))


zenith = 90.8333


def get_event(event_date: date, latitude: float, longitude: float, event: str):
    # 1. first calculate the day of the year
    day_of_year = (event_date - date(year=event_date.year, month=1, day=1)).days + 1

    # 2. convert the longitude to hour value and calculate an approximate time
    lngHour = longitude / 15

    if event == "sunrise":
        t = day_of_year + ((6 - lngHour) / 24)
    if event == "sunset":
        t = day_of_year + ((18 - lngHour) / 24)

    # 3. calculate the Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    # 4. calculate the Sun's true longitude
    L = (M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) + 282.634) % 360

    # 5a. calculate the Sun's right ascension
    right_ascension = atan(0.91764 * tan(L))
    if right_ascension < -360:
        sys.exit("TODO handle right_ascension < -360 " + str(right_ascension))
    if right_ascension > 360:
        sys.exit("TODO handle right_ascension > 360 " + str(right_ascension))

    # 5b. right ascension value needs to be in the same quadrant as L
    Lquadrant = (math.floor(L / 90)) * 90
    RAquadrant = (math.floor(right_ascension / 90)) * 90
    right_ascension = right_ascension + (Lquadrant - RAquadrant)

    # 5c. right ascension value needs to be converted into hours
    right_ascension = right_ascension / 15

    # 6. calculate the Sun's declination
    sinDec = 0.39782 * sin(L)
    cosDec = cos(asin(sinDec))

    # 7a. calculate the Sun's local hour angle
    cosH = (cos(zenith) - (sinDec * sin(latitude))) / (cosDec * cos(latitude))

    # 7b. finish calculating H and convert into hours
    if event == "sunrise":
        H = (360 - acos(cosH)) / 15
    if event == "sunset":
        H = (acos(cosH)) / 15

    # print("H", H)

    # 8. calculate local mean time of rising/setting
    T = H + right_ascension - (0.06571 * t) - 6.622

    # 9. adjust back to UTC
    UT = (T - lngHour)

    hour = math.floor(UT)
    minute = round(60 * ((UT % 1) % 1))
    if minute == 60:
        minute = 59
    secs = math.floor(60 * ((60 * ((UT % 1) % 1)) % 1))

    event_time = datetime(
        year=event_date.year, month=event_date.month, day=event_date.day,
        hour=hour % 24, minute=minute, second=0,
        tzinfo=pytz.utc
    )

    if event == "sunrise":
        if hour < 0:
            event_time = event_time - timedelta(days=1)

    if event == "sunset":
        if hour > 0:
            event_time = event_time + timedelta(days=1)

    return event_time


def get_sunrise(sunrise_date: date, latitude: float, longitude: float):
    return get_event(event_date=sunrise_date, latitude=latitude, longitude=longitude, event="sunrise")


def get_sunset(sunset_date: date, latitude: float, longitude: float):
    return get_event(event_date=sunset_date, latitude=latitude, longitude=longitude, event="sunset")


def pretty_pretty_sun(event_date, latitude, longitude, tz):
    sunrise = get_sunrise(event_date, latitude=latitude, longitude=longitude).astimezone(tz)
    sunset = get_sunset(event_date, latitude=latitude, longitude=longitude).astimezone(tz)

    data = []
    for _ in range((24 * 4) + 1):
        data.append("·")

    sunrise_seconds = sunrise.hour * 60 * 60 + sunrise.minute * 60
    sunset_seconds = sunset.hour * 60 * 60 + sunset.minute * 60

    sunrise_frac = int((sunrise_seconds / 86400) * len(data))
    sunset_frac = int((sunset_seconds / 86400) * len(data))

    data[sunrise_frac] = "|"
    data[sunset_frac] = "|"

    for x in range(sunrise_frac + 1, sunset_frac):
        data[x] = "*"

    print(event_date, "\t\t", "{:%H:%M:%S}".format(sunrise), "\t", *data, "\t", "{:%H:%M:%S}".format(sunset), sep="")


print("Auckland")
for i in range((date(2019, 12, 31) - date(2019, 1, 1)).days + 1):
    day = date(2019, 1, 1) + timedelta(days=i)
    pretty_pretty_sun(day, latitude=-36.8485, longitude=174.7633, tz=pytz.timezone("Pacific/Auckland"))

# print("Oslo")
# for i in range((date(2019, 12, 31) - date(2019, 1, 1)).days + 1):
#     day = date(2019, 1, 1) + timedelta(days=i)
#     pretty_pretty_sun(day, latitude=59.9139, longitude=10.7522, tz=pytz.timezone("Europe/Oslo"))
#
# print("Tromsø")
# for i in range((date(2019, 12, 31) - date(2019, 1, 1)).days + 1):
#     day = date(2019, 4, 1) + timedelta(days=i)
#     pretty_pretty_sun(day, latitude=69.6492, longitude=18.9553, tz=pytz.timezone("Europe/Oslo"))
