import numpy as np
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
from datetime import datetime
import io
import base64
import mplfinance as mpf

# get list of candlestick patterns
candle_names = ta.get_function_groups()['Pattern Recognition']

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

    # Create a structured NumPy array
    dtype = [("open", float), ("close", float), ("high", float), ("low", float), ("date", int)]
    numpy_array = np.array(list(zip(open, close, high, low, date)), dtype=dtype)

    pattern_function = getattr(ta, patternName)
    pattern_result = pattern_function(numpy_array['open'], numpy_array['close'], numpy_array['high'], numpy_array['low'])
    return pattern_result

def createChart(history):
    data_dict_list = []
    for stock in history:
        data_dict_list.append({
            'open': stock.open,
            'close': stock.close,
            'high': stock.high,
            'low': stock.low,
            'date': stock.date,
            'volume': stock.volume
    })
    
    df = pd.DataFrame(data_dict_list)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df.set_index('date', inplace=True)
    print(df)
    mpf.plot(df)

    # Save the plot as an image in memory
    buffer = io.BytesIO()
    mpf.savefig(buffer, format='png')
    buffer.seek(0)
    mpf.close()

    # Convert the image to a base64-encoded string
    data_uri = base64.b64encode(buffer.read()).decode('utf-8')

    return data_uri

# Create a Trading Class
# Create a Buy and Sell Class

class Trader:
    def __init__(self, initialAmount):
        self.balance = initialAmount
        self.stocksHolding = {
            'stock' : 'numberHeld'
        }
    def displayAccount(self):
        print(self.balance)
