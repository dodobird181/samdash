from datetime import datetime, timedelta
from os import listdir, remove
from typing import Callable

from pandas import DataFrame, read_csv

CACHE_DIR = "cached_data"
DT_SAVE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def _cache_df(obj_name: str, df: DataFrame, delta: timedelta) -> None:
    """
    Cache a dataframe with some name to use for later retrieval. Overrides previous caches with same obj_name.
    """
    for filename in listdir(CACHE_DIR):
        if filename.split("_")[0] == obj_name:
            remove(f"{CACHE_DIR}/{filename}")
    lifespan = datetime.now() + delta
    filename = f"{CACHE_DIR}/{obj_name}_{lifespan.strftime(DT_SAVE_FORMAT)}.csv"
    df.to_csv(filename, index=True)


def get_cached_df(obj_name: str, data_provider: Callable[[], DataFrame], delta: timedelta) -> DataFrame:
    """
    Get a cached dataframe, or else use the given data provider to generate the data and cache it.
    """
    cachepath = None
    cachefilename = None
    for filename in listdir(CACHE_DIR):
        # try to find the cache file
        if filename.split("_")[0] == obj_name:
            cachepath = f"{CACHE_DIR}/{filename}"
            cachefilename = filename
            break
    if cachepath is None:
        # base-case 1: no cached data
        data = data_provider()
        _cache_df(obj_name, data, delta)
        return data
    assert cachefilename is not None
    if datetime.strptime(cachefilename.split("_")[1].split(".")[0], DT_SAVE_FORMAT) <= datetime.now():
        # base-case 2: cache entry has expired
        data = data_provider()
        _cache_df(obj_name, data, delta)
        return data
    # otherwise, the cache should be valid
    return read_csv(cachepath, index_col=0, parse_dates=True)
