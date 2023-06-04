import requests
import sys
import random
sys.path.append('../')
from main import getStock

stock = input("Enter the symbol of the stock you would like to PUT: ")
stock = getStock(stock)
stockJson = {"name": stock.info['longName'], "symbol": stock.info['symbol'], "exchange": stock.info['exchange'], "avg_volume": stock.info['regularMarketVolume'], "high_52_weekly": stock.info['fiftyTwoWeekHigh'], "low_52_weekly": stock.info['fiftyTwoWeekLow']}
print(stockJson)
headers = {"Content-Type": "application/json"}
   
#generate a random id
id = random.randint(0, 9999999)   
id = str(id)

response = requests.put('http://localhost:5000/stock/' + id, json=stockJson, headers=headers)
print(response.json())



