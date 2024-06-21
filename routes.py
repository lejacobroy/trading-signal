from flask import request, jsonify
from database import get_db_connection, add_stock, add_alert, get_stocks
from flask import render_template, redirect, url_for


def configure_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            action = request.form.get("action")
            if action == "add_stock":
                symbol = request.form.get("symbol")
                add_stock(symbol)
                return render_template("index.html", message="Stock added successfully")
            elif action == "set_alert":
                stock_id = request.form.get("stock_id")
                indicator = request.form.get("indicator")
                threshold = request.form.get("threshold")
                add_alert(stock_id, indicator, threshold)
        stocks = get_stocks()
        print(stocks)
        indicators = ["MACD", "BB", "RSI", "SMA", "MA Cross"]
        return render_template(
            "index.html", stocks=stocks, indicators=indicators, message=None
        )
