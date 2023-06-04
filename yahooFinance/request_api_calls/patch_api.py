import requests

id = input("Enter the id of the stock you would like to update: ")

response =requests.get('http://localhost:5000/stock/' + id)
jsonResponse = response.json()
print(jsonResponse)

print("Update the values as needed. If you do not want to update a value, leave it blank.")
name= input("name: " + jsonResponse['name'] + "---> ")
symbol = input("symbol: " + jsonResponse['symbol'] + "---> ")
exchange = input("exchange: " + jsonResponse['exchange'] + "---> ")
high_52_weekly = input("high_52_weekly: " + str(jsonResponse['high_52_weekly']) + "---> ")
low_52_weekly = input("low_52_weekly: " + str(jsonResponse['low_52_weekly']) + "---> ")
avg_volume = input("avg_volume: " + str(jsonResponse['avg_volume']) + "---> ")  

if name == "":
    name = jsonResponse['name']
if symbol == "":
    symbol = jsonResponse['symbol']
if exchange == "":
    exchange = jsonResponse['exchange']
if high_52_weekly == "":
    high_52_weekly = jsonResponse['high_52_weekly']
if low_52_weekly == "":
    low_52_weekly = jsonResponse['low_52_weekly']
if avg_volume == "":
    avg_volume = jsonResponse['avg_volume']

headers = {"Content-Type": "application/json"}
response =requests.patch('http://localhost:5000/stock/' + id, json={"id": id, "name": name, "symbol": symbol, "exchange": exchange, "high_52_weekly": high_52_weekly, "low_52_weekly": low_52_weekly, "avg_volume": avg_volume}, headers=headers)
print(response.json())



