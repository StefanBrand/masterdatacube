from datetime import datetime
from util import date_interval_endpoints

def test_one_month():
    assert date_interval_endpoints(datetime(2019,9,1), datetime(2019,9,30), 16) == \
        [datetime(2019,9,1,0,0), datetime(2019,9,15,23,59,59),
         datetime(2019,9,16,0,0), datetime(2019,9,30,23,59,59)]

def test_two_months():
    assert date_interval_endpoints(datetime(2019,9,1), datetime(2019,10,31),16) == \
        [datetime(2019,9,1,0,0), datetime(2019,9,15,23,59,59),
         datetime(2019,9,16,0,0), datetime(2019,9,30,23,59,59),
         datetime(2019,10,1,0,0), datetime(2019,10,15,23,59,59),
         datetime(2019,10,16,0,0), datetime(2019,10,31,23,59,59)]

def test_starts_on_2nd():
    assert date_interval_endpoints(datetime(2019,9,2), datetime(2019,9,30), 16) == \
        [datetime(2019,9,2,0,0), datetime(2019,9,15,23,59,59),
         datetime(2019,9,16,0,0), datetime(2019,9,30,23,59,59)]

def test_starts_on_15th():
    assert date_interval_endpoints(datetime(2019,9,15), datetime(2019,9,30), 16) == \
        [datetime(2019,9,15,0,0), datetime(2019,9,15,23,59,59),
         datetime(2019,9,16,0,0), datetime(2019,9,30,23,59,59)]

def test_starts_on_16th():
    assert date_interval_endpoints(datetime(2019,9,16), datetime(2019,9,30), 16) == \
        [datetime(2019,9,16,0,0), datetime(2019,9,30,23,59,59)]

def test_starts_on_17th():
    assert date_interval_endpoints(datetime(2019,9,17), datetime(2019,9,30), 16) == \
        [datetime(2019,9,17,0,0), datetime(2019,9,30,23,59,59)]

def test_starts_on_last():
    assert date_interval_endpoints(datetime(2019,9,30), datetime(2019,9,30), 16) == \
        [datetime(2019,9,30,0,0), datetime(2019,9,30,23,59,59)]

def test_ends_on_29th():
    assert date_interval_endpoints(datetime(2019,9,1), datetime(2019,9,29), 16) == \
        [datetime(2019,9,1,0,0), datetime(2019,9,15,23,59,59),
         datetime(2019,9,16,0,0), datetime(2019,9,29,23,59,59)]

def test_ends_on_16th():
    assert date_interval_endpoints(datetime(2019,9,1), datetime(2019,9,16), 16) == \
        [datetime(2019,9,1,0,0), datetime(2019,9,15,23,59,59),
         datetime(2019,9,16,0,0), datetime(2019,9,16,23,59,59)]

def test_ends_on_15th():
    assert date_interval_endpoints(datetime(2019,9,1), datetime(2019,9,15), 16) == \
        [datetime(2019,9,1,0,0), datetime(2019,9,15,23,59,59)]

def test_ends_on_14th():
    assert date_interval_endpoints(datetime(2019,9,1), datetime(2019,9,14), 16) == \
        [datetime(2019,9,1,0,0), datetime(2019,9,14,23,59,59)]

def test_starts_and_ends_somewhere():
    assert date_interval_endpoints(datetime(2019,9,4), datetime(2019,9,25), 16) == \
        [datetime(2019,9,4,0,0), datetime(2019,9,15,23,59,59),
         datetime(2019,9,16,0,0), datetime(2019,9,25,23,59,59)]

def test_new_year():
    assert date_interval_endpoints(datetime(2019,12,16), datetime(2020,1,15), 16) == \
        [datetime(2019,12,16,0,0), datetime(2019,12,31,23,59,59),
         datetime(2020,1,1,0,0), datetime(2020,1,15,23,59,59)]

def test_different_day_of_new_interval():
    assert date_interval_endpoints(datetime(2019,9,1), datetime(2019,9,30), 10) == \
        [datetime(2019,9,1,0,0), datetime(2019,9,9,23,59,59),
         datetime(2019,9,10,0,0), datetime(2019,9,30,23,59,59)]