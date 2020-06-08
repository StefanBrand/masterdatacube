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
        and not dates[-1].day == d-1
        else dates
    )

    for i in range(1,len(dates),2):
        dates[i] = dates[i]+rdelta(hour=23, minute=59, second=59)
    return dates