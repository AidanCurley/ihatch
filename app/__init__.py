"""Create the application"""
from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from config import config

load_dotenv()


csrf = CSRFProtect()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    csrf.init_app(app)
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
