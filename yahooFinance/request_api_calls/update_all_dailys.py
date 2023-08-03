# run this script at the end of the day to update all daily data
# for all stocks in the database
# :)


# ISSUES:
# when the daily data gets loaded, a new id is created but it may create a duplicate id.

import requests
import pandas as pd
import numpy as np
import datetime
import time
import os
import sys
import requests
import json
import yfinance as yf

#create an update function 
def update_daily_data(recent_date, todays_date, recent_daily_id, stock_id):
    # get the stock history
    response = requests.get('http://localhost:5000/stock/' + str(stock_id) + '/0')
    # parse the stock history from the most recent date to todays date
    stock_history = json.loads(response.text)
    # get the last date in the stock history
    last_date = stock_history[-1]['date']
    # get the last id in the stock history
    last_id = stock_history[-1]['id']
    # get the stock symbol
    response = requests.get('http://localhost:5000/stock/' + str(stock_id))
    stock_symbol = response.json()['symbol']
    # get the stock history from the last date to todays date
    stock = yf.Ticker(stock_symbol)
    stock.info
    # increase recent_date by 1 day
    recent_date = datetime.datetime.strptime(str(recent_date), "%Y%m%d")
    recent_date = recent_date + datetime.timedelta(days=1)
    recent_date = recent_date.strftime("%Y%m%d")
    # convert YYYYMMDD to YYYY-MM-DD
    recent_date = str(recent_date)
    recent_date = recent_date[:4] + '-' + recent_date[4:6] + '-' + recent_date[6:]
    todays_date = str(todays_date)
    todays_date = todays_date[:4] + '-' + todays_date[4:6] + '-' + todays_date[6:]
    stock = stock.history(start=recent_date, end=todays_date)
    # put the stock history into the database
    for i in range(len(stock)):
        recent_daily_id += 1
        # print(recent_daily_id)
        date = datetime.datetime.strptime(str(stock.index[i].date()), '%Y-%m-%d')
        year = date.year
        month = date.month
        day = date.day
        date_integer = year * 10000 + month * 100 + day
        stockJson = {"date": date_integer, "open": stock.iloc[i]['Open'], "high": stock.iloc[i]['High'], "low": stock.iloc[i]['Low'], "close": stock.iloc[i]['Close'], "volume": stock.iloc[i]['Volume']}
        stockJson = json.dumps(stockJson)
        stockJson = json.loads(stockJson)
        headers = {"Content-Type": "application/json"}
        response = requests.put('http://localhost:5000/stock/' + str(stock_id) + '/' + str(recent_daily_id), json=stockJson, headers=headers)
        print(response.json())
    return 0

#get todays date
today = datetime.date.today()
# turn it into an integer with the format YYYYMMDD
today = int(today.strftime("%Y%m%d"))
#get the stock id
response = requests.get('http://localhost:5000/stock/0')
stock_list = response.json()
#seperate the stock id's
stock_list_id = []
for stock in stock_list:
    stock_list_id.append(stock['id'])
#send request to get the daily data for each stock
for stock in stock_list_id:
    response = requests.get('http://localhost:5000/stock/' + str(stock) + '/0')
    daily_data = json.loads(response.text)
    #search the daily data for the most recent date
    most_recent_id = 0
    most_recent_date = daily_data[0]['date']
    stock_id = daily_data[0]['stock_id']
    for day in daily_data:
        if day['date'] > most_recent_date:
            most_recent_date = day['date']
            most_recent_id = day['id']
    #compare the most recent date to todays date
    if most_recent_date < today:
        #if the most recent date is not today, then update the daily data
        print("updating data")
        update_daily_data(most_recent_date, today, most_recent_id, stock_id)
    else:
        #if the most recent date is today, then do nothing
        print("already up to date")

