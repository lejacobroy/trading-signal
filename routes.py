from flask import request, jsonify
from database import get_db_connection, add_stock, add_alert, get_stocks, get_stock, del_stock, get_alerts, get_alert, del_alert
from flask import render_template, redirect, url_for


def configure_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", message=None)
        
    @app.route("/stocks", methods=["GET"])
    def stocks():
        message = None
        stocks = get_stocks()
        # https://open.substack.com/pub/bmpro/p/four-bitcoin-indicators-one-comprehensive?utm_source=email&redirect=app-store
        indicators = ["MACD", "BB", "RSI", "SMA", "MA Cross", "MVRM", "True Price", "STH Realized Price Indicator", "Reserve Risk Indicator", "Pi Cycle Top", "Terminal Price Indicator"]
        return render_template("stocks.html", stocks=stocks, indicators=indicators, message=message)
    
    @app.route("/stocks/<id>", methods=["GET"])
    def stock(id):
        message = None
        stock = get_stock(id=id)
        return render_template("stock.html", stock=stock, message=message)
    
    @app.route("/stocks/remove/<id>", methods=["POST"])
    def stock_remove(id):
        message = None
        if request.method == "POST":
            stock_id = request.form.get("stock_id")
            del_stock(stock_id)
            message="Stock removed successfully"
        return redirect(url_for("stocks", message=message))
    
    @app.route("/stocks/add", methods=["POST"])
    def stock_add():
        message = None
        if request.method == "POST":
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
        alerts = get_alerts()
        stocks = get_stocks()
        indicators = ["MACD", "BB", "RSI", "SMA", "MA Cross"]
        return render_template("alerts.html", alerts=alerts, stocks=stocks, indicators=indicators, message=message)
    
    @app.route("/alerts/<id>", methods=["GET"])
    def alert(id):
        message = None
        alert = get_alert(id=id)
        indicators = ["MACD", "BB", "RSI", "SMA", "MA Cross"]
        return render_template("alert.html", alert=alert, message=message)
    
    @app.route("/alerts/remove/<id>", methods=["POST"])
    def alert_remove(id):
        message = None
        if request.method == "POST":
            alert_id = request.form.get("alert_id")
            del_alert(alert_id)
            message="Alert removed successfully"
        return redirect(url_for("alerts", message=message))
        
    @app.route("/alerts/add", methods=["POST"])
    def alert_add():
        message = None
        if request.method == "POST":
            stock_id = request.form.get("stock_id")
            indicator = request.form.get("indicator")
            threshold = request.form.get("threshold")
            add_alert(stock_id, indicator, threshold)
            message="Alert added successfully"
        return redirect(url_for("alerts", message=message))