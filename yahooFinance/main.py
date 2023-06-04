import yfinance as yf
import pandas as pd
import classes as classes

def getStock(symbol):
    return yf.Ticker(symbol)

def getStockHistory(symbol, period):
    stock = yf.Ticker(symbol)
    stock.info
    stock = stock.history(period=period)
    return stock

stock = getStockHistory("AAPL", "1y")

print(stock)




