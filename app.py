import traceback
import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('Stock Prices of US companies')

st.sidebar.write("""
# GAFA Stock Prices
This is a stock price acquisition tool. You can specify the number of days to display from the following options.
""")

st.sidebar.write("""
## Select the number of days to display
""")

days = st.sidebar.slider('Number of days', 1, 50, 20)       #range

st.write(f"""
### GAFA's stock price over the past **{days}days**
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()  # Container for info

    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')  # fetch stock infomation
        hist.index = hist.index.strftime('%d %B %Y')  # change date format
        hist = hist[['Close']]  # Get only the latest stock price
        hist.columns = [company]  # put name of company on the column
        hist = hist.T  # Turn the table sideways
        hist.index.name = 'Name'  # change the name
        df = pd.concat([df, hist])  # update
    return df

try:
    st.sidebar.write("""
    ## Select the Stock Price Range
    """)

    ymin, ymax = st.sidebar.slider(
        'Specify the range',
        0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'Apple': 'AAPL',
        'Facebook': 'FB',
        'Google': 'GOOGL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Amazon': 'AMZN'

    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        'Select companies',
        list(df.index),
        ['Google', 'Apple', 'Facebook', 'Amazon']
    )

    if not companies:
        st.error('Please select at least one company')
    else:
        data = df.loc[companies]
        st.write("### Stock Price(USD)", data.sort_index())  # organaize to alphabetical order
        data = data.T.reset_index()  # organaize to take data for graph
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )  # organaize to take data for graph

    chart = (  # Chart
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )

    st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(
        "Oops! Something went wrong. Please check the error details below:"
    )
    st.write(e)
    st.write(traceback.format_exc())

