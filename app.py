from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    exchange = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Stock(name = {name}, symbol = {symbol}, exchange = {exchange})"
    
#create another model for stock prices
class StockPriceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #foreign key to stock model
    stock_id = db.Column(db.Integer, db.ForeignKey('stock_model.id'), nullable=False)
    open = db.Column(db.Integer, nullable=False)
    close = db.Column(db.Integer, nullable=False)
    high = db.Column(db.Integer, nullable=False)
    low = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Stock(open = {open}, close = {close}, high = {high}, low = {low}, date = {date})"

stock_put_args = reqparse.RequestParser()
stock_put_args.add_argument("name", type=str, help="Name of the stock is required", required=True)
stock_put_args.add_argument("symbol", type=str, help="Symbol of the stock is required", required=True)
stock_put_args.add_argument("exchange", type=str, help="Exchange symbol of the stock is required", required=True)
# stock_put_args.add_argument("open", type=int, help="Open required", required=True)
# stock_put_args.add_argument("close", type=int, help="Close required", required=True)
# stock_put_args.add_argument("high", type=int, help="High required", required=True)
# stock_put_args.add_argument("low", type=int, help="Low required", required=True)
# stock_put_args.add_argument("date", type=int, help="Date required", required=True)



# serialization is the process of converting the state of an object into a form that can be persisted or transported
# this is a dictionary that will define the fields from StockModel into a JSON format(serialization)
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'symbol': fields.String,
    'exchange': fields.String
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stock")
def stock():
    headers = []
    for header in resource_fields:
        headers += header
    # get all the data from the database
    data = StockModel.query.all()
    return render_template("stock-analyzer.html", headers = headers, data = data)

class StockTracker(Resource):
    # when we return, take this return value and serialize it using resource_fields
    @marshal_with(resource_fields)
    def get(self, stock_id):
        result = StockModel.query.filter_by(id=stock_id).first()
        if not result:
            abort(404, message='Could not find stock with that id')
        return result
    
    @marshal_with(resource_fields)
    def put(self, stock_id):
        args = stock_put_args.parse_args()
        result = StockModel.query.filter_by(id=stock_id).first()
        if result:
            abort(409, message='Stock id taken')
        stock = StockModel(id = stock_id, name = args['name'], symbol = args['symbol'], exchange = args['exchange'])
        db.session.add(stock)
        db.session.commit()
        return stock, 201
    
    def patch(self, stock_id):
        args = stock_put_args.parse_args()
        return 400

    def delete(self, stock_id):
        return '', 400
    
api.add_resource(StockTracker, "/stock/<int:stock_id>")

if __name__ == '__main__':
    # debug=True will reload the server when you make changes to the code
    app.run(debug=True, port=5000)