import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# %matplotlib inline

aapl = yf.Ticker('AAPL')

days = 20                                           #range
hist = aapl.history(period=f'{days}d')
hist.index = hist.index.strftime('%d %B %Y')        #change date format
hist = hist[['Close']]                              #Get only the latest stock price
hist.columns = ['apple']                            #put name of company on the column
hist = hist.T                                       #Turn the table sideways
hist.index.name = 'Name'                            #change the name
hist
