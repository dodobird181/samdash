from bs4 import BeautifulSoup
from requests import get as GET


def _get_page_bid(url: str) -> float:
    """
    Get the bid price from a kitco "/charts" page.
    """
    html = GET(url, headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    price = soup.select('h3[class*="tracking"]')
    return float(price[0].text.replace(",", ""))


def latest_gold_price() -> float:
    return _get_page_bid("https://www.kitco.com/charts/gold")


def latest_silver_price() -> float:
    return _get_page_bid("https://www.kitco.com/charts/silver")
