import logging

from flask import Flask

from src.routes.future_price_scrapper import future_price_api as future_price_bp
from src.routes.payout import payout_api as payout_bp
from src.routes.welcome import welcome_api as welcome_bp


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(future_price_bp)
    app.register_blueprint(payout_bp)
    app.register_blueprint(welcome_bp)
    
    return app
