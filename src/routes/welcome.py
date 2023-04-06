import logging

from flask import Blueprint

log = logging.getLogger(__name__)
welcome_api = Blueprint("welcome", __name__)


@welcome_api.route("/welcome", methods=["GET"])
def welcome():
    log.debug("Welcome to Payout Calculation Service")

    return "Welcome to Payout Calculation Service"