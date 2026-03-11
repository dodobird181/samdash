from numpy.random import randn
from pandas import DataFrame
from streamlit import area_chart, columns, header, session_state, set_page_config, title
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000, key="counter")
set_page_config(layout="wide")

if "count" not in session_state:
    session_state.count = 0

title("Hello world!")

header("Foo bar!", divider="rainbow")

col1, col2 = columns([1, 1])

with col1:
    chart_data = DataFrame(randn(20 + session_state.count, 3), columns=["a", "b", "c"])
    area_chart(data=chart_data, x_label="Poop factor")

with col2:
    chart_data = DataFrame(randn(20, 3), columns=["a", "b", "c"])
    area_chart(data=chart_data, x_label="Poop factor")


session_state.count += 1
