import numpy as np
import talib as ta
import requests
import json
# import yahooFinance.request_api_calls.get_api as get

# get list of candlestick patterns
candle_names = ta.get_function_groups()['Pattern Recognition']

# get
# id = input("Enter the day of the stock you would like to look up (Enter 0 to get all):")
# id = int(id)

# response = requests.get('http://localhost:5000/stock/' + get.id + '/' + str(id))
# #print(response.json())

# data = json.loads(response.text)

# # Extract object properties into separate arrays
# open = np.array([obj["open"] for obj in data])
# close = np.array([obj["close"] for obj in data])
# high = np.array([obj["high"] for obj in data])
# low = np.array([obj["low"] for obj in data])
# date = np.array([obj["date"] for obj in data])
# id = np.array([obj["id"] for obj in data])

# # Create a structured NumPy array
# dtype = [("open", float), ("close", float), ("high", float), ("low", float), ("date", int), ("id", int)]
# numpy_array = np.array(list(zip(open, close, high, low, date, id)), dtype=dtype)
# #print(numpy_array)

# for pattern in candle_names:
#     print(pattern)
#     pattern_function = getattr(ta, pattern)
#     pattern_result = pattern_function(numpy_array['open'], numpy_array['close'], numpy_array['high'], numpy_array['low'])
#     print(pattern_result)

def candlestickPattern(patternName, dailyStockData):
    if not patternName:
        return 
    if not dailyStockData:
        return print("No daily stock data for this stock")
    # Extract object properties into separate arrays
    open = np.array([obj.open for obj in dailyStockData])
    close = np.array([obj.close for obj in dailyStockData])
    high = np.array([obj.high for obj in dailyStockData])
    low = np.array([obj.low for obj in dailyStockData])
    date = np.array([obj.date for obj in dailyStockData])
    id = np.array([obj.id for obj in dailyStockData])

    # Create a structured NumPy array
    dtype = [("open", float), ("close", float), ("high", float), ("low", float), ("date", int), ("id", int)]
    numpy_array = np.array(list(zip(open, close, high, low, date, id)), dtype=dtype)

    pattern_function = getattr(ta, patternName)
    pattern_result = pattern_function(numpy_array['open'], numpy_array['close'], numpy_array['high'], numpy_array['low'])
    return pattern_result





