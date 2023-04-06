
import logging

from flask import Blueprint, make_response, request

from scripts.scraper import get_future_price

log = logging.getLogger(__name__)
future_price_api = Blueprint("future_price", __name__)


@future_price_api.route("/future_price", methods=["GET"])
def future_price_route():
    paylaod = dict(request.args)
    result = get_future_price()
    response = make_response(result)
    response.mimetype = "text/json"
    return response, 200
