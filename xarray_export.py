from datetime import datetime
from dateutil.relativedelta import relativedelta as rdelta
from dateutil.rrule import rrule, MONTHLY
import logging
import numpy as np
from shapely.geometry import shape
from pandas import to_datetime, IntervalIndex
import xarray as xr

from mapchete_satellite.exceptions import EmptyStackException
from mapchete_satellite.settings import SENTINEL2_BAND_INDEXES


logger = logging.getLogger(__name__)


def execute(
    mp,
    bands=[2, 3, 4, 5, 6, 7, 8, 9, 11, 12],
    resampling="cubic_spline",
    read_threads=1
):
    """
    Extract satellite data slices to 4D xarray.

    Inputs
    ------
    satellite_cube
        S2AWS or S2Mundi input

    Parameters
    ----------
    bands : int or list of int
        Indexes of bands considered.
    resampling : str (default: 'nearest')
        Resampling used when reading data.
    read_threads : 1
        Number of parallel read threads.

    Output
    ------
    xarray.DataArray
    """
    if "aoi" in mp.params["input"]:
        with mp.open("aoi") as aoi:
            if not len(aoi.read()):
                return "empty"

    with mp.open("satellite_cube") as sat:
        try:
            # create 4D xr.DataArray with named slice_ids and named bands
            in_cube = sat.read_cube(
                indexes=bands,
                resampling=resampling,
                mask_clouds=True,
                threads=read_threads
            )
            band_names = [SENTINEL2_BAND_INDEXES[sat.processing_level][i] for i in bands]
            logger.debug("%s/%s slices valid" % (len(in_cube), len(sat.source_data)))
            logger.debug("slice_ids %s", ", ".join(in_cube.slice_ids))
            logger.debug("band_names %s", ", ".join(band_names))

            cube = xr.DataArray(
                # apply masks and swap "bands" and "timestamp" axes
                in_cube.data.transpose(1, 0, 2, 3),
                # named dimension indexes
                coords={
                    "bands": [b.split('_')[0] for b in band_names],
                    "timestamps": list(in_cube.timestamps),
                },
                # named dimensions
                dims=("bands", "timestamps", "x", "y"),
                # additional attributes
            )

            # temporarily convert to xarray.DataSet
            cube = cube.to_dataset("bands")

            # Generate time intervals
            starttime = datetime(*min(in_cube.timestamps).timetuple()[:3], 0, 0, 0)
            endtime = datetime(*max(in_cube.timestamps).timetuple()[:3], 0, 0, 0)

            # new interval starts at day 16 of month
            eps = date_interval_endpoints(*sat._time_range, 16)
            int_idx = IntervalIndex.from_arrays(eps[::2], eps[1::2])
            avg_cube = cube.groupby_bins('timestamps', bins=int_idx).mean('timestamps')
            avg_cube = avg_cube.rename({'timestamps_bins': 'time'}) # xcube Dataset spec
            avg_cube.coords['time'] = int_idx.mid # zarr cannot have IntervalIndex as coords

            for idx, (ic1, ic2) in ics.items():
                if ic1 in avg_cube and ic2 in avg_cube:
                    # 2**16
                    avg_cube[idx] = calculate_index(avg_cube[ic1], avg_cube[ic2]) * 65335

            # CVI calculation
            if "B03" in avg_cube and "B05" in avg_cube and "B08" in avg_cube:
                avg_cube['CVI'] = (avg_cube.B08 * avg_cube.B05 / avg_cube.B03**2) * 1000

            # Typing conforming to SH Mass output
            avg_cube = avg_cube.astype(np.uint16)

            # convert to xarray.DataArray again for writing
            return avg_cube.to_array("bands")

        except EmptyStackException:
            logger.debug("tile empty")
            return "empty"


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
        and not dates[-1].day == 15
        else dates
    )

    for i in range(1,len(dates),2):
        dates[i] = dates[i]+rdelta(hour=23, minute=59, second=59)
    return dates


def calculate_index(a, b):
    """Calculate one of the ices indexes."""
    # stretch [-1,+1] to [0,1]
    return ((a - b) / (a + b) + 1) / 2

# index components
ics = {
    "NDVI": ["B08", "B04"],
    "GNDVI": ["B08", "B03"],
    "BNDVI": ["B08", "B02"],
    "NDSI": ["B11", "B12"],
    "NDWI": ["B03", "B08"]
}
