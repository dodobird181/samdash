"""
Fetches live spot prices for all instruments and writes to cache.

    python src/price_fetcher.py
"""

from datetime import timedelta
from logging import getLogger
from time import sleep

from config import INSTRUMENTS
from data_sources.utils.caching import cache_price

logger = getLogger(__name__)


def fetch_prices() -> None:
    for instrument in INSTRUMENTS:
        try:
            price = instrument.price_fetcher()
            # cache the price for 10 minutes (longer than the quick refresh rate on purpose)
            cache_price(f"{instrument.key}price", price, timedelta(minutes=10))
            logger.info("%sprice: cached %s", instrument.key, price)
        except Exception as e:
            logger.error("%sprice: %s", instrument.key, e)


if __name__ == "__main__":
    min_sleep = min(inst.price_delta.total_seconds() for inst in INSTRUMENTS)
    logger.info("Initializing real-time price fetcher with refresh at %s seconds.", min_sleep)
    while True:
        fetch_prices()
        logger.debug("sleeping %ds...", min_sleep)
        sleep(min_sleep)
