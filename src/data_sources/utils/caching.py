from datetime import datetime, timedelta
from os import listdir, remove, replace
from os.path import exists
from typing import Callable

from pandas import DataFrame, read_csv

CACHE_DIR = "cached_data"
DT_SAVE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def cache_df(obj_name: str, df: DataFrame, delta: timedelta) -> None:
    """
    Cache a dataframe with some name to use for later retrieval. Overrides previous caches with same obj_name.
    """
    lifespan = datetime.now() + delta
    final = f"{CACHE_DIR}/{obj_name}_{lifespan.strftime(DT_SAVE_FORMAT)}.csv"
    tmp = f"{final}.tmp"
    df.to_csv(tmp, index=True)
    replace(tmp, final)
    for filename in listdir(CACHE_DIR):
        if filename.split("_")[0] == obj_name and filename != f"{obj_name}_{lifespan.strftime(DT_SAVE_FORMAT)}.csv":
            filepath = f"{CACHE_DIR}/{filename}"
            if exists(filepath):
                remove(filepath)


def read_cached_df(obj_name: str) -> DataFrame | None:
    """
    Read a cached dataframe. Returns None if not found or expired.
    Does not fetch or write — intended for use by the Streamlit app.
    """
    for filename in listdir(CACHE_DIR):
        if filename.split("_")[0] == obj_name:
            expiry = datetime.strptime(filename.split("_")[1].split(".")[0], DT_SAVE_FORMAT)
            if expiry <= datetime.now():
                return None
            return read_csv(f"{CACHE_DIR}/{filename}", index_col=0, parse_dates=True)
    return None


def cache_price(key: str, price: float, delta: timedelta) -> None:
    lifespan = datetime.now() + delta
    final = f"{CACHE_DIR}/{key}_{lifespan.strftime(DT_SAVE_FORMAT)}.txt"
    tmp = f"{final}.tmp"
    with open(tmp, "w") as f:
        f.write(str(price))
    replace(tmp, final)
    for filename in listdir(CACHE_DIR):
        if filename.split("_")[0] == key and filename != f"{key}_{lifespan.strftime(DT_SAVE_FORMAT)}.txt":
            filepath = f"{CACHE_DIR}/{filename}"
            if exists(filepath):
                remove(filepath)


def read_cached_price(key: str) -> float | None:
    for filename in listdir(CACHE_DIR):
        if filename.split("_")[0] == key and filename.endswith(".txt"):
            expiry = datetime.strptime(filename.split("_")[1].split(".")[0], DT_SAVE_FORMAT)
            if expiry <= datetime.now():
                return None
            with open(f"{CACHE_DIR}/{filename}") as f:
                return float(f.read())
    return None
