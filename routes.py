from flask import request, jsonify
from database import (
    add_stock, 
    add_alert, 
    get_stocks, 
    get_stock, 
    del_stock, 
    get_alerts, 
    get_alert, 
    del_alert,
    get_indicators,
    get_periods,
    get_intervals,
    get_alerts_details,
    get_alerts_by_stock,
    get_alert_result
)
from alerts import check_alerts
from models import Alert
from flask import render_template, redirect, url_for

def get_base_data():
    stocks = get_stocks()
    alerts = get_alerts()
    alerts_details = get_alerts_details()
    indicators = get_indicators()
    periods = get_periods()
    intervals = get_intervals()
    data = {
        "stocks": stocks,
        "alerts": alerts,
        "indicators": indicators,
        "periods": periods,
        "intervals": intervals,
        "alerts_details": alerts_details
    }
    return data

def configure_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", message=None)
        
    @app.route("/stocks", methods=["GET"])
    def stocks():
        message = None
        data = get_base_data()
        # https://open.substack.com/pub/bmpro/p/four-bitcoin-indicators-one-comprehensive?utm_source=email&redirect=app-store
        return render_template("stocks.html", data=data, message=message)
    
    @app.route("/stocks/<id>", methods=["GET"])
    def stock(id):
        message = None
        data = get_base_data()
        stock = get_stock(id=id)
        data['stock_alerts'] = get_alerts_by_stock(id)
        data["alerts_results"] = []
        for alert in data['stock_alerts']:
            result = {
                'stock_symbol': stock['symbol'],
                'indicator_name': alert['indicator_name'],
                'period_name': alert['period_name'],
                'interval_name': alert['interval_name'],
                'action': alert['action'],
                'threshold': alert['threshold'],
                'result': get_alert_result(id=alert['id'], stock=stock['id'])
            }
            data['alerts_results'].append(result)
        return render_template("stock.html", stock=stock, data=data, message=message)
    
    @app.route("/stocks/check/<id>", methods=["POST"])
    def stock_check(id):
        message = None
        data = get_base_data()
        stock = get_stock(id=id)
        check_alerts()
        message="Stock checked successfully"
        return redirect(url_for("stock", id=id, message=message))
    
    @app.route("/stocks/remove/<id>", methods=["POST"])
    def stock_remove(id):
        message = None
        del_stock(id)
        message="Stock removed successfully"
        return redirect(url_for("stocks", message=message))
    
    @app.route("/stocks/add", methods=["POST"])
    def stock_add():
        message = None
        symbol = request.form.get("symbol")
        if not symbol:
            message="Please enter a valid symbol"
            return redirect(url_for("stocks", message=message))
        add_stock(symbol)
        message="Stock added successfully"
        return redirect(url_for("stocks", message=message))
    
    @app.route("/alerts", methods=["GET"])
    def alerts():
        message = None
        data = get_base_data()
        return render_template("alerts.html", data=data, message=message)
    
    @app.route("/alerts/<id>", methods=["GET"])
    def alert(id):
        message = None
        alert = get_alert(id=id)
        data = get_base_data()
        return render_template("alert.html", alert=alert, data=data, message=message)
    
    @app.route("/alerts/remove/<id>", methods=["POST"])
    def alert_remove(id):
        message = None
        print(id)
        del_alert(id)
        message="Alert removed successfully"
        return redirect(url_for("alerts", message=message))
        
    @app.route("/alerts/add", methods=["POST"])
    def alert_add():
        message = None
        alert = Alert(
            stock_id=request.form.get("stock_id"),
            indicator_id=request.form.get("indicator"),
            period_id=request.form.get("period"),
            interval_id=request.form.get("interval"),
            action=request.form.get("action"),
            threshold=request.form.get("threshold")
        )
        add_alert(alert=alert)
        message="Alert added successfully"
        return redirect(url_for("alerts", message=message))