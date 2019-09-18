import unittest
from datetime import date, datetime

import pytz

from sun import get_sunrise, get_sunset


class TestSun(unittest.TestCase):
    def test_Tokyo_sunrise(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=14, hour=20, minute=23, tzinfo=pytz.utc),
            get_sunrise(sunrise_date=date(year=2019, month=9, day=15), latitude=35.6762, longitude=139.6503)
        )

    def test_Auckland_sunrise(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=14, hour=18, minute=22, tzinfo=pytz.utc),
            get_sunrise(sunrise_date=date(year=2019, month=9, day=15), latitude=-36.8485, longitude=174.7633)
        )

    def test_Denver_sunrise(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=15, hour=12, minute=41, tzinfo=pytz.utc),
            get_sunrise(sunrise_date=date(year=2019, month=9, day=15), latitude=39.7392, longitude=-104.9903)
        )

    def test_Rio_sunrise(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=15, hour=8, minute=50, tzinfo=pytz.utc),
            get_sunrise(sunrise_date=date(year=2019, month=9, day=15), latitude=-22.9068, longitude=-43.1729)
        )

    def test_Tokyo_sunset(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=16, hour=8, minute=48, tzinfo=pytz.utc),
            get_sunset(sunset_date=date(year=2019, month=9, day=16), latitude=35.6762, longitude=139.6503)
        )

    def test_Auckland_sunset(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=15, hour=6, minute=11, tzinfo=pytz.utc),
            get_sunset(sunset_date=date(year=2019, month=9, day=15), latitude=-36.8485, longitude=174.7633)
        )

    def test_Denver_sunset(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=16, hour=1, minute=9, tzinfo=pytz.utc),
            get_sunset(sunset_date=date(year=2019, month=9, day=15), latitude=39.7392, longitude=-104.9903)
        )

    def test_Rio_sunset(self):
        self.assertEqual(
            datetime(year=2019, month=9, day=15, hour=20, minute=47, tzinfo=pytz.utc),
            get_sunset(sunset_date=date(year=2019, month=9, day=15), latitude=-22.9068, longitude=-43.1729)
        )

    def test_Tromso_sunrise(self):
        self.assertEqual(
            datetime(2019, 5, 17, hour=1, minute=22, tzinfo=pytz.utc),
            get_sunrise(date(2019, 5, 17), latitude=69.6492, longitude=18.9553)
        )

    def test_Tromso_sunset(self):
        self.assertEqual(
            datetime(2019, 5, 18, hour=12, minute=17, tzinfo=pytz.utc),
            get_sunset(date(2019, 5, 17), latitude=69.6492, longitude=18.9553)
        )
