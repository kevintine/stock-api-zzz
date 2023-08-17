# right now the issue is the id seems to already have been taken so sqlalchemy is giving me an error when I try to commit 
# another record into it. seems like you cannot have multiple same id's otherwise it gives an error? still not understanding 

from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import requests
import candlesticks
import csv
import pandas as pd
import yahooFinance.main as yfAPI
import numpy as np
import json
import talib as ta

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    exchange = db.Column(db.String(10), nullable=False)
    avg_volume = db.Column(db.Integer, nullable=True)
    high_52_weekly = db.Column(db.Float, nullable=True)
    low_52_weekly = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f"Stock(name = {self.name}, symbol = {self.symbol}, exchange = {self.exchange})"
    
#create another model for stock prices
class StockPriceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #foreign key to stock model
    stock_id = db.Column(db.Integer, db.ForeignKey('stock_model.id'), nullable=False)
    day_id = db.Column(db.Integer, nullable=False)
    open = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

    # Remove unique constraint on columns if present
    __table_args__ = ()

    def __repr__(self):
        return f"Stock(open = {self.open}, close = {self.close}, high = {self.high}, low = {self.low}, date = {self.date}, volume = {self.volume})"
    

with app.app_context():
    db.create_all()

stock_put_args = reqparse.RequestParser()
stock_put_args.add_argument("name", type=str, help="Name of the stock is required", required=True)
stock_put_args.add_argument("symbol", type=str, help="Symbol of the stock is required", required=True)
stock_put_args.add_argument("exchange", type=str, help="Exchange symbol of the stock is required", required=True)
stock_put_args.add_argument("high_52_weekly", type=float, help="52 week high required", required=True)
stock_put_args.add_argument("low_52_weekly", type=float, help="52 week low required", required=True)
stock_put_args.add_argument("avg_volume", type=int, help="Average volume required", required=True)

stockPrice_put_args = reqparse.RequestParser()
stockPrice_put_args.add_argument("open", type=float, help="Open price is required", required=True)
stockPrice_put_args.add_argument("close", type=float, help="Close price is required", required=True)
stockPrice_put_args.add_argument("high", type=float, help="High price is required", required=True)
stockPrice_put_args.add_argument("low", type=float, help="Low price is required", required=True)
stockPrice_put_args.add_argument("date", type=int, help="Date is required", required=True)
stockPrice_put_args.add_argument("volume", type=int, help="Volume is required", required=True)

# serialization is the process of converting the state of an object into a form that can be persisted or transported
# this is a dictionary that will define the fields from StockModel into a JSON format(serialization)
resource_fields_StockModel = {
    'id': fields.Integer,
    'name': fields.String,
    'symbol': fields.String,
    'exchange': fields.String,
    'high_52_weekly': fields.Float,
    'low_52_weekly': fields.Float,
    'avg_volume': fields.Integer
}

resource_fields_StockPriceModel = {
    'id': fields.Integer,
    'stock_id': fields.Integer,
    'open': fields.Float,
    'close': fields.Float,
    'high': fields.Float,
    'low': fields.Float,
    'date': fields.Integer,
    'volume': fields.Integer
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stock")
def stock():
    # get all the data from the database
    data = StockModel.query.all()
    # get input from html
    CDL = request.args.get('pattern')
    sign = []
    chart = []
    for stock in data:
        dailyData = StockPriceModel.query.filter_by(stock_id=stock.id).all()
        screener = candlesticks.candlestickPattern(CDL, dailyData)
        chart.append(candlesticks.createChart(dailyData))
        if screener is not None:
            lastDay = screener[-1]
        else:
            lastDay = 0
        if lastDay > 0:
            sign.append('Bullish')
        elif lastDay < 0:
            sign.append('Bearish')
        else:
            sign.append('Neutral')
    pair = zip(data, sign, chart)
    return render_template("stock-analyzer.html", candlesticks = candlesticks.candle_names, pair = pair)

@app.route("/analysis")
def analysis():
    # take a button press on a pattern
    CDL = request.args.get('param')
    data = StockModel.query.all()
    # search a stock for all instances of that pattern
    # return the dates of those patterns
    # create a function that takes the date and depending on how many days after if pricec went up or down
    return render_template("analysis.html", data = data)

@app.route("/fortune500")
def fortuneFiveHundred():
    CDL = request.args.get('pattern')
    #get a list of the fortune 500
    #read the csv
    df = pd.read_csv("data/stockList.csv", usecols = [0])
    #turn datframe into a list
    stockList = df.iloc[:,0].to_list()
    updatedList = []
    #add a ".to" to the end of each stock so that yfinance can properly search
    for stock in stockList:
        if isinstance(stock, float):
            continue
        updatedList.append(stock + ".TO")
    sign = []
    #pass the list through to yfinance to get data
    for stock in updatedList:
        try:
            stockData = yfAPI.getStockHistory(stock, "1y")
        except:
            print("An Exception Occured Pulling From The CSV")
        #convert pandas dataframe to json
        #issue: not converting all dataframes, is it the dataframe or my for loop
        #issue update: turns out im only getting one row in the dataframe
        stockJson = []
        for i in range(len(stockData)):
            stockJson.append({"open": stockData.iloc[i]['Open'], "high": stockData.iloc[i]['High'], "low": stockData.iloc[i]['Low'], "close": stockData.iloc[i]['Close']})

        stockJson = json.dumps(stockJson)
        stockJson = json.loads(stockJson)
        # convert json to numpy array
        # stockJson = json.dumps(stockJson)
        # stockJson = json.loads(stockJson)
        ##################### create another screener to handle the data
        # Extract object properties into separate arrays
        open = [item["open"] for item in stockJson]
        close = [item["close"] for item in stockJson]
        high = [item["high"] for item in stockJson]
        low = [item["low"] for item in stockJson]
        # Create a structured NumPy array
        dtype = [("open", float), ("close", float), ("high", float), ("low", float)]
        numpy_array = np.array(list(zip(open, close, high, low)), dtype=dtype)
        try:
            if CDL is None:
                continue
            pattern_function = getattr(ta, CDL)
            pattern_result = pattern_function(numpy_array['open'], numpy_array['close'], numpy_array['high'], numpy_array['low'])
            if pattern_result is not None:
                lastDay = pattern_result[-1]
            else:
                lastDay = 0
            if lastDay > 0:
                sign.append('Bullish')
            elif lastDay < 0:
                sign.append('Bearish')
            else:
                sign.append('Neutral')
        except:
            print("An Exception Occured During Screening")
    pair = zip(stockList, sign)

    return render_template("tmxStocksWatchList.html", pair=pair, candlesticks = candlesticks.candle_names)

class StockTracker(Resource):
    # when we return, take this return value and serialize it using resource_fields
    @marshal_with(resource_fields_StockModel)
    def get(self, stock_id):
        if stock_id == 0:
             result = StockModel.query.all()
             return result
        result = StockModel.query.filter_by(id=stock_id).first()
        if not result:
            abort(404, message='Could not find stock with that id')
        return result
    
    @marshal_with(resource_fields_StockModel)
    def put(self, stock_id):
        args = stock_put_args.parse_args()
        result = StockModel.query.filter_by(id=stock_id).first()
        if result:
            abort(409, message='Stock id taken')
        stock = StockModel(id = stock_id, name = args['name'], symbol = args['symbol'], exchange = args['exchange'], high_52_weekly = args['high_52_weekly'], low_52_weekly = args['low_52_weekly'], avg_volume = args['avg_volume'])
        db.session.add(stock)
        db.session.commit()
        return stock, 201
    
    @marshal_with(resource_fields_StockModel)
    def patch(self, stock_id):
        args = stock_put_args.parse_args()
        result = StockModel.query.filter_by(id=stock_id).first()
        if not result:
            abort(404, message='Could not find stock with that id')
        # get json payload
        if "name" in args:
            result.name = args['name']
        if "symbol" in args:
            result.symbol = args['symbol']
        if "exchange" in args:
            result.exchange = args['exchange']
        if "high_52_weekly" in args:
            result.high_52_weekly = args['high_52_weekly']
        if "low_52_weekly" in args:
            result.low_52_weekly = args['low_52_weekly']
        if "avg_volume" in args:
            result.avg_volume = args['avg_volume']
        db.session.commit()
        return result, 201
    
    @marshal_with(resource_fields_StockModel)
    def delete(self, stock_id):
        result = StockModel.query.filter_by(id=stock_id).first()
        if not result:
            abort(404, message='Could not find stock with that id')
        db.session.delete(result)
        db.session.commit()
        return 204
    
class StockDayTracker(Resource):

    @marshal_with(resource_fields_StockPriceModel)
    def get(self, day_id, web_stock_id):
        if day_id == 0:
            result = StockPriceModel.query.filter_by(stock_id=web_stock_id).all()
            return result
        result = StockModel.query.filter_by(id=web_stock_id).first()
        if not result:
            abort(404, message='Could not find stock with that id')
        result = StockPriceModel.query.filter_by(day_id=day_id, stock_id=web_stock_id).first()
        if not result:
            abort(404, message='Could not find day with that id')
        return result

    @marshal_with(resource_fields_StockPriceModel)
    def put(self, day_id, web_stock_id):
        day_id = int(day_id)
        print(day_id)
        web_stock_id = int(web_stock_id)
        args = stockPrice_put_args.parse_args()
        result = StockModel.query.filter_by(id=web_stock_id).first()
        if not result:
            abort(404, message='No stock with that id')
        result = StockPriceModel.query.filter_by(stock_id = web_stock_id, day_id = day_id).first()
        if result:
            abort(404, message='Day id taken')
        daily = StockPriceModel(day_id = day_id, stock_id = web_stock_id, open = args['open'], close = args['close'], low = args['low'], high = args['high'], date = args['date'], volume = args['volume'])
        print(daily)
        db.session.add(daily)
        db.session.commit()
        return daily, 201
    
    @marshal_with(resource_fields_StockPriceModel)
    def patch(self, day_id, web_stock_id):
        result = StockModel.query.filter_by(id=web_stock_id).first()
        if not result:
            abort(404, message='Could not find stock with that id')
        result = StockPriceModel.query.filter_by(id=day_id).first()
        if not result:
            abort(404, message='Could not find day with that id')
        args = stockPrice_put_args.parse_args()
        # get json payload
        if "open" in args:
            result.open = args['open']
        if "close" in args:
            result.close = args['close']
        if "low" in args:
            result.low = args['low']
        if "high" in args:
            result.high = args['high']
        if "date" in args:
            result.date = args['date']
        if "volume" in args:
            result.volume = args['volume']
        db.session.commit()
        return result, 201
    
    @marshal_with(resource_fields_StockPriceModel)
    def delete(self, day_id, web_stock_id):
        if day_id == 0:
            result = StockPriceModel.query.filter_by(stock_id=web_stock_id).all()
            for day in result:
                db.session.delete(day)
            db.session.commit()
            return 204
        result = StockModel.query.filter_by(id=web_stock_id).first()
        if not result:
            abort(404, message='Could not find stock with that id')
        result = StockPriceModel.query.filter_by(day_id=day_id).first()
        if not result:
            abort(404, message='Could not find day with that id')
        db.session.delete(result)
        db.session.commit()
        return 204

api.add_resource(StockTracker, "/stock/<int:stock_id>")
api.add_resource(StockDayTracker, "/stock/<int:web_stock_id>/<int:day_id>")

if __name__ == '__main__':
    # debug=True will reload the server when you make changes to the code
    app.run(debug=True, port=5000)
