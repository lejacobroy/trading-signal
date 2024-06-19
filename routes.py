from flask import request, jsonify
from database import get_db
from models import Stock, Alert

def configure_routes(app):
    @app.route('/stocks', methods=['GET', 'POST'])
    def manage_stocks():
        db = get_db()
        if request.method == 'POST':
            data = request.json
            stock = Stock(symbol=data['symbol'])
            db.session.add(stock)
            db.session.commit()
            return jsonify({'message': 'Stock added'}), 201
        else:
            stocks = Stock.query.all()
            return jsonify([stock.to_dict() for stock in stocks])

    @app.route('/alerts', methods=['GET', 'POST'])
    def manage_alerts():
        db = get_db()
        if request.method == 'POST':
            data = request.json
            alert = Alert(stock_id=data['stock_id'], indicator=data['indicator'], threshold=data['threshold'])
            db.session.add(alert)
            db.session.commit()
            return jsonify({'message': 'Alert added'}), 201
        else:
            alerts = Alert.query.all()
            return jsonify([alert.to_dict() for alert in alerts])