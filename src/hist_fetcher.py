"""
Fetches historical OHLCV data for all instruments/timeframes and writes to cache.

    python src/fetcher.py
"""

from logging import getLogger
from time import sleep

from config import (
    GOLD_INSTRUMENT,
    INSTRUMENTS,
    SPY_INSTRUMENT,
    SPY_TO_GOLD_30Y_KEY,
    THIRTY_YEAR_MONTHLY_TIMEFRAME,
    US_TEN_YEAR_TREASURY_KEY,
    cache_key,
)
from data_sources.utils.caching import cache_df, read_cached_df
from data_sources.yfinance import get_yfinance_data

logger = getLogger(__name__)


def fetch_all() -> None:

    # financial instrument grid defined in config
    for instrument in INSTRUMENTS:
        for timeframe in instrument.timeframes:
            key = cache_key(instrument, timeframe)
            try:
                data = get_yfinance_data(instrument.ticker, period=timeframe.period, interval=timeframe.interval)
                if data.empty:
                    logger.warning("%s: empty response, skipping", key)
                    continue
                cache_df(key, data, timeframe.hist_delta)
                logger.debug("%s: cached %d rows", key, len(data))
            except Exception as e:
                logger.error("%s: %s", key, e)

    # download spy dataframes (3-month daily + 30-year monthly)
    for timeframe in [THIRTY_YEAR_MONTHLY_TIMEFRAME]:
        key = cache_key(SPY_INSTRUMENT, timeframe)
        try:
            data = get_yfinance_data(SPY_INSTRUMENT.ticker, period=timeframe.period, interval=timeframe.interval)
            if data.empty:
                logger.warning("%s: empty response, skipping", key)
                continue
            cache_df(key, data, timeframe.hist_delta)
            logger.debug("%s: cached %d rows", key, len(data))
        except Exception as e:
            logger.error("%s: %s", key, e)

    # also fetch gold for the 30-year monthly timeframe
    gold_30y_key = cache_key(GOLD_INSTRUMENT, THIRTY_YEAR_MONTHLY_TIMEFRAME)
    try:
        data = get_yfinance_data(
            GOLD_INSTRUMENT.ticker,
            period=THIRTY_YEAR_MONTHLY_TIMEFRAME.period,
            interval=THIRTY_YEAR_MONTHLY_TIMEFRAME.interval,
        )
        if not data.empty:
            cache_df(gold_30y_key, data, THIRTY_YEAR_MONTHLY_TIMEFRAME.hist_delta)
            logger.debug("%s: cached %d rows", gold_30y_key, len(data))
        else:
            logger.warning("%s: empty response, skipping", gold_30y_key)
    except Exception as e:
        logger.error("%s: %s", gold_30y_key, e)

    # compute and cache the 30-year monthly SPY-to-gold ratio
    gold_30y_df = read_cached_df(gold_30y_key)
    spy_30y_df = read_cached_df(cache_key(SPY_INSTRUMENT, THIRTY_YEAR_MONTHLY_TIMEFRAME))
    if gold_30y_df is not None and not gold_30y_df.empty and spy_30y_df is not None and not spy_30y_df.empty:
        ratio_30y = (
            spy_30y_df[["Open", "High", "Low", "Close"]].div(gold_30y_df[["Open", "High", "Low", "Close"]]).dropna()
        )
        cache_df(SPY_TO_GOLD_30Y_KEY, ratio_30y, THIRTY_YEAR_MONTHLY_TIMEFRAME.hist_delta)
        logger.debug("%s: cached %d rows", SPY_TO_GOLD_30Y_KEY, len(ratio_30y))
    else:
        logger.warning("%s: missing gold or spy data, skipping", SPY_TO_GOLD_30Y_KEY)

    # fetch 30-year monthly US 10-year treasury yield (^TNX)
    try:
        treasury_df = get_yfinance_data("^TNX", period="max", interval="1mo")
        if not treasury_df.empty:
            cache_df(US_TEN_YEAR_TREASURY_KEY, treasury_df, THIRTY_YEAR_MONTHLY_TIMEFRAME.hist_delta)
            logger.debug("%s: cached %d rows", US_TEN_YEAR_TREASURY_KEY, len(treasury_df))
        else:
            logger.warning("%s: empty response, skipping", US_TEN_YEAR_TREASURY_KEY)
    except Exception as e:
        logger.error("%s: %s", US_TEN_YEAR_TREASURY_KEY, e)


if __name__ == "__main__":
    min_sleep = min(tf.hist_delta.total_seconds() for inst in INSTRUMENTS for tf in inst.timeframes)
    while True:
        fetch_all()
        logger.info("sleeping %ds...", min_sleep)
        sleep(min_sleep)
