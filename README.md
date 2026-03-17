# [Samdash](https://sammorris.ca/samdash)
Samdash is a [Streamlit](https://streamlit.io/) webapp for aggregating news and economic data that I build for fun. It tracks Gold, Silver, Oil, the S&P 500, AP News, and more. It is also a work-in-progress.

[<img src="https://raw.githubusercontent.com/dodobird181/samdash/refs/heads/main/thumbnail.png" alt="Loading thumbnail..." width="800" style="margin-bottom: 20px;"/>](https://sammorris.ca/samdash)

### Motivation
The world has been getting increasingly volatile over the past couple of years, and I've found that the stock-market has reflected this volatility as well. The problem is, the more I learn about how markets function (and disfunction), the more webpages I found myself checking to catch a glimpse of what I consider to be "the full-picture."

This project is my attempt at a solution: put every data source I want to check in one place!

### Goals
I originally wanted to create a cool-looking terminal dashboard using [Dashing](https://github.com/FedericoCeratto/dashing) but I found that it was [not actively maintained](https://github.com/FedericoCeratto/dashing/issues/26#issuecomment-2299140052). There are other TUI libraries out there, but they seemed a little overkill to me. So I abandoned the idea and decided to learn something I'd never used before: Streamlit.

Some of my goals for this project were to:
- Visualize stock tickers at different time-intervals on the same page;
- Learn more about server-side rendering in Python using Streamlit;
- Figure out how to plot stock-market candle data with real-time updates;
- Cache market data so I don't get rate-limited or cause too many requests to be sent;
- Make the dashboard modular and easily extensible so I can add to it in the future.

### Design
A fairly reliable way to make the dashboard easily extensible in the future, in my opinion, is by enforcing a strong separation of concerns. Two seperate Python processes run to fetch data alongside the main process that handles server-side rendering. This way, blocking API calls don't intefere with app rendering, and the app doesn't have to worry about state, since it's read-only.

The reason I separated _real-time_ and _historical_ data fetching into two processes is because fetching historical data can sometimes take longer than the small interval used for fetching real-time data. This would make it so that when historical data is being fetched the expectation around the frequency of live price-updates would be broken, which is undesireable.

You can see a rough outline of the design below:

<img src="https://raw.githubusercontent.com/dodobird181/samdash/refs/heads/main/design-diagram.png" alt="Loading diagram..." width="800" style="margin-bottom: 20px;"/>