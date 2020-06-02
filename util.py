def date_interval_endpoints(starttime, endtime, day_of_new_interval):
    """
    Return a list of half-month endpoints.

    Keyword arguments:
    - starttime: datetime or date
    - endtime: datetime or date
    - day_of_new_interval: int

    Returns:
    - dates: list(datetime)
    """

    from datetime import datetime
    from dateutil.relativedelta import relativedelta as rdelta
    from dateutil.rrule import rrule, MONTHLY
    from pandas import to_datetime

    starttime = datetime(*starttime.timetuple()[:3],0,0)
    endtime = datetime(*endtime.timetuple()[:3],0,0)
    d=day_of_new_interval

    dates = list(rrule(MONTHLY, dtstart=starttime, until=endtime, bymonthday=[1,d-1,d,-1]))
    dates = (
        [starttime] + dates
        if not dates[0].day == 1 and not dates[0].day == d
        else dates
    )
    dates = (
        dates + [endtime]
        if not dates[-1].day == to_datetime(dates[-1]).daysinmonth
        and not dates[-1].day == 15)
        else dates
    )

    for i in range(1,len(dates),2):
        dates[i] = dates[i]+rdelta(hour=23, minute=59, second=59)
    return dates


from datetime import datetime

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
