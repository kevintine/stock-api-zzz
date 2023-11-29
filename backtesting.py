# This file contains all the types of stock strategy backtesting

import numpy as np
import talib as ta
import requests
import json
import matplotlib.pyplot as plt
import yfinance as yf

# Creating a class for finding different candlestick patterns
# Will mostly be returning entire stock data array's (Takes long may have to create something to return single days)
class FindCandlestickPattern:
    def __init__(self, stockData):
        self.stockData = stockData
        self.highLowAverage = self.findHighLowAverage()
    def displayRawData(self):
        print(self.stockData)
    # Takes an array of days
    def historyColor(self):
        color = []
        for day in self.stockData:
            if day.open < day.close:
                color.append('G')
            else:
                color.append('R')
        return color
    # Takes single day 
    def dayColor(self, day):
        if day.open < day.close:
            return "G"
        return "R"
    def findHighLowAverage(self):
        averageHighLow = 0
        average = 0
        for day in self.stockData:
            avg = day.high - day.low
            if (avg < 0):
                avg = avg * -1
            averageHighLow += avg
        averageHighLow = averageHighLow / 255
        return averageHighLow
    # Takes an array of days
    # Returns an array of boolean values. 'True' having a hammer on that day
    def CDLhammer(self):
        arrayOfHammers = []
        for day in self.stockData:
            x = day.high - day.low
            x = x * .6
            x = x + day.low
            if day.open > x and day.close > x:
                arrayOfHammers.append(True)
            else:
                arrayOfHammers.append(False)
        return arrayOfHammers
    def getDatesForPattern(self, patternName, patternArray):
        if patternName == False:
            return "No patternName for getDatesForPattern()"
        dates = []
        pair = zip(self.stockData, patternArray)
        for day, TrueFalse in pair:
            if TrueFalse == True:
                dates.append(day)
        return dates

# Checks overall trend of the dates
# def trend(stock, length):
