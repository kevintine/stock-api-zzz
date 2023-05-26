import yfinance as yf
import pandas as pd
import classes as classes

def getStock(symbol):
    return yf.Ticker(symbol)

def getStockHistory(symbol, period, interval):
    stock = getStock(symbol)
    return stock.history(period=period, interval=interval)




