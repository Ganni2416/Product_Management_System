from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .logger import setup_logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging(app)
    db.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

