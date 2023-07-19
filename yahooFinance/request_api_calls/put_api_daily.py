import requests
import get_api as get
import sys
import json
from datetime import datetime
sys.path.append('../')
from main import getStockHistory

get

stock = get.response.json()

stockData = getStockHistory(stock['symbol'], "1y")

print("Populating database with stock data...")

date = datetime.strptime(str(stockData.index[2].date()), '%Y-%m-%d')
year = date.year
month = date.month
day = date.day
date_integer = year * 10000 + month * 100 + day

for i in range(len(stockData)):
    day_id = str(i + 1)
    date = datetime.strptime(str(stockData.index[i].date()), '%Y-%m-%d')
    year = date.year
    month = date.month
    day = date.day
    date_integer = year * 10000 + month * 100 + day
    stockJson = {"date": date_integer, "open": stockData.iloc[i]['Open'], "high": stockData.iloc[i]['High'], "low": stockData.iloc[i]['Low'], "close": stockData.iloc[i]['Close'], "volume": stockData.iloc[i]['Volume']}
    stockJson = json.dumps(stockJson)
    stockJson = json.loads(stockJson)
    headers = {"Content-Type": "application/json"}
    response = requests.put('http://localhost:5000/stock/' + str(stock['id']) + '/' + day_id, json=stockJson, headers=headers)
    print(response.json())







