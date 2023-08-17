# This file contains all the types of stock strategy backtesting

import numpy as np
import talib as ta
import requests
import json
import matplotlib.pyplot as plt
import yfinance as yf

# Check for color
def color(day):
    color = ''
    if day[1]['Open'] < day[1]['Close']:
        color = 'green'
    else:
        color = 'red'
    return color

# Check if the day is considered a hammer
def CDLhammer(day):
    x = day[1]['High'] - day[1]['Low']
    x = x * .6
    x = x + day[1]['Low']
    if (color(day) == 'red'):
        return False
    if (day[1]['Open'] > x):
        return True
    return False