import yfinance as yf
import pandas as pd
import classes as classes

airCanada = yf.Ticker("AC.TO")
print(airCanada.history(period="1y", interval="1d").tail(1))
airCanadaObject = airCanada.history(period="1y", interval="1d").tail(1).to_dict()
print(airCanadaObject)