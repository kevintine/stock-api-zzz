class CandleStick:
    def __init__(self, open, high, low, close, volume, timestamp):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.timestamp = timestamp
        self.type = None
    def candleStickType(self):
        return self.type

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.candleSticks = []
    def returnOpenCloseDiffernecialAverage(self):
        pass
