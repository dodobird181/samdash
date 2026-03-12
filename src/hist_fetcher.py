"""
Fetches historical OHLCV data for all instruments/timeframes and writes to cache.

    python src/fetcher.py
"""

from logging import getLogger
from time import sleep

from config import INSTRUMENTS, cache_key
from data_sources.utils.caching import cache_df
from data_sources.yfinance import get_yfinance_data

logger = getLogger(__name__)


def fetch_all() -> None:
    for instrument in INSTRUMENTS:
        for timeframe in instrument.timeframes:
            key = cache_key(instrument, timeframe)
            try:
                data = get_yfinance_data(instrument.ticker, period=timeframe.period, interval=timeframe.interval)
                if data.empty:
                    logger.warning("%s: empty response, skipping", key)
                    continue
                cache_df(key, data, timeframe.hist_delta)
                logger.info("%s: cached %d rows", key, len(data))
            except Exception as e:
                logger.error("%s: %s", key, e)


if __name__ == "__main__":
    min_sleep = min(tf.hist_delta.total_seconds() for inst in INSTRUMENTS for tf in inst.timeframes)
    while True:
        fetch_all()
        logger.info("sleeping %ds...", min_sleep)
        sleep(min_sleep)
