import numpy as np
import talib as ta
import requests
import json
import matplotlib.pyplot as plt

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
    id = np.array([obj.id for obj in dailyStockData])

    # Create a structured NumPy array
    dtype = [("open", float), ("close", float), ("high", float), ("low", float), ("date", int), ("id", int)]
    numpy_array = np.array(list(zip(open, close, high, low, date, id)), dtype=dtype)

    pattern_function = getattr(ta, patternName)
    pattern_result = pattern_function(numpy_array['open'], numpy_array['close'], numpy_array['high'], numpy_array['low'])
    return pattern_result

#determine if day is green or red stick
#takes one day
def greenOrRed(day):
    color = ''
    if day[1]['Open'] < day[1]['Close']:
        color = 'green'
    else:
        color = 'red'
    return color

#analysis function to check a stock for three green days
#takes historical stock data
def threeGreenDays(history):
    dates = []
    #go through history and find when there were three green bars in a row
    trend = []
    for day in history.iterrows():
        #check for a green bar
        check = greenOrRed(day)
        if check == 'green':
            trend.append(check)
        else:
            trend.clear()
        # if length of the trend is 3, get the date of the day and put it into dates
        if len(trend) == 3:
            dates.append(day[0])
    #give me the end date of those three green bars
    #put them in a list in the dates variable
    return dates

# candlestick chart
def candlestickChart(history):
    print(history)
    # create figure
    plt.figure()
    #define width of candlestick elements
    width = .4
    width2 = .05
    #define up and down prices
    up = history[history['Open'] >= history['Close']]
    down = history[history['Close'] , history['Open']]
    #define colors
    col1 = 'green'
    col2 = 'red'
    #plot up prices
    plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
    plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
    plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)

    #plot down prices
    plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
    plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
    plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)

    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    #display candlestick chart
    plt.show()
    return 0


