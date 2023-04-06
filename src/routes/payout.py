
import logging

from flask import Blueprint, make_response, request

from src.controllers.payout import payout

log = logging.getLogger(__name__)
payout_api = Blueprint("payout", __name__)


@payout_api.route("/payout", methods=["GET"])
def payout_route():
    paylaod = dict(request.args)
    result = payout(paylaod)
    response = make_response(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.mimetype = "text/json"
    return response, 200
