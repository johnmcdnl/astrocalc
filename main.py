import datetime
import math
import sys
import time
from datetime import datetime, timedelta


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


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


def main_rise(date):
    N1 = math.floor(275 * date.month / 9)
    N2 = math.floor((date.month + 9) / 12)
    N3 = (1 + math.floor((date.year - 4 * math.floor(date.year / 4) + 2) / 3))
    N = N1 - (N2 * N3) + date.day - 30

    lngHour = longitude / 15

    t = N + ((6 - lngHour) / 24)

    M = (0.9856 * t) - 3.289

    L = (M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) + 282.634) % 360

    RA = atan(0.91764 * tan(L))
    if RA < -360:
        sys.exit("TODO handle RA < -360", RA)
    if RA > 360:
        sys.exit("TODO handle RA > 360", RA)

    Lquadrant = (math.floor(L / 90)) * 90
    RAquadrant = (math.floor(RA / 90)) * 90
    RA = RA + (Lquadrant - RAquadrant)

    RA = RA / 15

    sinDec = 0.39782 * sin(L)
    cosDec = cos(asin(sinDec))

    cosH = (cos(zenith) - (sinDec * sin(latitude))) / (cosDec * cos(latitude))

    H = (360 - acos(cosH)) / 15

    T = H + RA - (0.06571 * t) - 6.622

    UT = (T - lngHour) % 24

    hrs = math.floor(UT)
    mins = math.floor(60 * ((UT % 1) % 1))
    secs = math.floor(60 * ((60 * ((UT % 1) % 1)) % 1))

    rise = datetime(date.year, date.month, date.day, hrs, mins, secs)

    return datetime_from_utc_to_local(rise)


def main_set(date):
    N1 = math.floor(275 * date.month / 9)
    N2 = math.floor((date.month + 9) / 12)
    N3 = (1 + math.floor((date.year - 4 * math.floor(date.year / 4) + 2) / 3))
    N = N1 - (N2 * N3) + date.day - 30

    lngHour = longitude / 15

    t = N + ((18 - lngHour) / 24)

    M = (0.9856 * t) - 3.289

    L = (M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) + 282.634) % 360

    RA = atan(0.91764 * tan(L))
    if RA < -360:
        sys.exit("TODO handle RA < -360", RA)
    if RA > 360:
        sys.exit("TODO handle RA > 360", RA)

    Lquadrant = (math.floor(L / 90)) * 90
    RAquadrant = (math.floor(RA / 90)) * 90
    RA = RA + (Lquadrant - RAquadrant)

    RA = RA / 15

    sinDec = 0.39782 * sin(L)
    cosDec = cos(asin(sinDec))

    cosH = (cos(zenith) - (sinDec * sin(latitude))) / (cosDec * cos(latitude))

    H = acos(cosH) / 15

    T = H + RA - (0.06571 * t) - 6.622

    UT = (T - lngHour) % 24

    hrs = math.floor(UT)
    mins = math.floor(60 * ((UT % 1) % 1))
    secs = math.floor(60 * ((60 * ((UT % 1) % 1)) % 1))

    set = datetime(date.year, date.month, date.day, hrs, mins, secs)

    return datetime_from_utc_to_local(set)


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def main():
    for date in date_range(datetime(2019, 9, 10), datetime(2019, 9, 20)):
        print("Auckland, New Zealand", "\t",
              date.strftime("%Y-%m-%d"), "\t",
              main_rise(date).strftime("%H:%M:%S"), "\t",
              main_set(date).strftime("%H:%M:%S"),
              )


zenith = 90.8333
longitude = 174.7633
latitude = -36.8485

main()
