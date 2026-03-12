from dataclasses import dataclass
from datetime import timedelta
from logging import INFO, WARNING, basicConfig, getLogger
from typing import Callable

from data_sources.investingdotcom import latest_brent_crude_oil_price
from data_sources.kitco import latest_gold_price, latest_silver_price

basicConfig(level=INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
# getLogger("yfinance").setLevel(WARNING)


@dataclass
class Timeframe:
    key: str  # short id, no underscores (used in cache key)
    label: str  # row header e.g. "1 Day"
    candle_label: str  # row sub-header e.g. "15 min candles"
    period: str  # yfinance period
    interval: str  # yfinance interval
    hist_delta: timedelta  # cache TTL for OHLCV data
    tick_fmt: str  # x-axis strftime format


@dataclass
class Instrument:
    key: str  # short id, no underscores (used in cache key)
    name: str  # display name
    ticker: str  # yfinance symbol
    color: str  # streamlit divider color
    price_fetcher: Callable[[], float]
    price_delta: timedelta  # cache TTL for spot price
    timeframes: list[Timeframe]


_TIMEFRAMES = [
    Timeframe(
        key="15min",
        label="1 Day",
        candle_label="15 min candles",
        period="1d",
        interval="15m",
        hist_delta=timedelta(minutes=5),
        tick_fmt="%-I:%M %p",
    ),
    Timeframe(
        key="4h",
        label="10 Day",
        candle_label="4 hour candles",
        period="10d",
        interval="4h",
        hist_delta=timedelta(minutes=5),
        tick_fmt="%b %d",
    ),
    Timeframe(
        key="1d",
        label="3 Month",
        candle_label="daily candles",
        period="90d",
        interval="1d",
        hist_delta=timedelta(minutes=30),
        tick_fmt="%b %d, %Y",
    ),
]

INSTRUMENTS: list[Instrument] = [
    Instrument(
        key="gold",
        name="Gold",
        ticker="GC=F",
        color="yellow",
        price_fetcher=latest_gold_price,
        price_delta=timedelta(seconds=5),
        timeframes=_TIMEFRAMES,
    ),
    Instrument(
        key="silver",
        name="Silver",
        ticker="SI=F",
        color="grey",
        price_fetcher=latest_silver_price,
        price_delta=timedelta(seconds=5),
        timeframes=_TIMEFRAMES,
    ),
    Instrument(
        key="oil",
        name="Brent Oil",
        ticker="BZ=F",
        color="red",
        price_fetcher=latest_brent_crude_oil_price,
        price_delta=timedelta(seconds=5),
        timeframes=_TIMEFRAMES,
    ),
]


def cache_key(instrument: Instrument, timeframe: Timeframe) -> str:
    return f"{instrument.key}{timeframe.key}"
