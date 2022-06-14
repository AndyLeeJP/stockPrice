import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt


days = 20                                           #range

tickers = {
    'Apple': 'AAPL',
    'Facebook': 'FB',
    'Google': 'GOOGL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Amazon': 'AMZN'

}

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

get_data(days, tickers)

companies = ['Apple', 'Facebook']
data = df.loc[companies]
data.sort_index() #organaize to alphabetical order
data = data.T.reset_index() #organaize to take data for graph
data = pd.melt(data, id_vars=['Date']).rename(
    columns={'value': 'Stock Prices(USD)'}
) #organaize to take data for graph


ymin, ymax = 100, 250

chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip= True)
    .encode(
        x="Date:T",
        y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
        color='Name:N'
    )
)
