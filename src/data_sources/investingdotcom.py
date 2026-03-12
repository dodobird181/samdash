from bs4 import BeautifulSoup
from requests import get as GET


def latest_brent_crude_oil_price() -> float:
    html = GET("https://ca.investing.com/commodities/crude-oil", headers={"User-Agent": "Mozilla/5.0"}).text
    soup = BeautifulSoup(html, "html.parser")
    price = soup.select('div[data-test*="instrument-price-last"]')
    return float(price[0].text.replace(",", ""))
