from flask import Flask
from routes import configure_routes
import os
from database import create_tables


def create_app():
    app = Flask(__name__)
    configure_routes(app)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["STATIC_FOLDER"] = os.path.join(os.getcwd(), "static")
    app.config["TEMPLATE_FOLDER"] = os.path.join(os.getcwd(), "templates")
    create_tables()
    return app
