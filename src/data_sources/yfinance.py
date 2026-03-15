from datetime import datetime

from pandas import DataFrame, MultiIndex
from yfinance import download
from yfinance import Ticker


class NoData(Exception):

    def __init__(self, instrument_name: str):
        self.instrument_name = instrument_name
        super().__init__(f'No yfinance data found for "{self.instrument_name}"!')


def get_yfinance_data(instrument_name: str, period="10d", interval="4h") -> DataFrame:

    data = download(instrument_name, period=period, interval=interval, progress=False)
    if data is None:
        raise NoData(instrument_name)
    if isinstance(data.columns, MultiIndex):
        # flatten MultiIndex columns if present
        data.columns = data.columns.get_level_values(0)
    data = data.astype(float)
    return data


def latest_spy_price():
    return round(Ticker("SPY").fast_info["last_price"], 2)
