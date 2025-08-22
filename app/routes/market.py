from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..schemas import SpotQuery
from ..services.market_data import get_spot_price
from ..utils import cached

bp = Blueprint("market", __name__)


@bp.route("/price/spot", methods=["GET"])
@cached(ttl=30)
def spot_price():
    try:
        params = SpotQuery(ticker=request.args.get("ticker", ""))
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "detail": ve.errors()}), 400

    price = get_spot_price(params.ticker)
    if price is None:
        return jsonify({"error": "not_found", "detail": f"No price for {params.ticker}"}), 404

    return jsonify({"ticker": params.ticker, "spot": price})