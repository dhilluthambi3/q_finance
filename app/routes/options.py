from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..schemas import OptionPriceRequest, OptionPriceResponse
from ..services.market_data import get_spot_price
from ..services.option_pricer import black_scholes_price, quantum_price_stub

bp = Blueprint("options", __name__)


@bp.route("/price/option/european", methods=["POST"])
def price_option_european():
    try:
        payload = OptionPriceRequest(**request.get_json(force=True))
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "detail": ve.errors()}), 400

    S0 = payload.S0 or get_spot_price(payload.ticker)
    if S0 is None:
        return (
            jsonify(
                {"error": "spot_unavailable", "detail": f"No spot for {payload.ticker}"}
            ),
            404,
        )

    if payload.method == "black_scholes":
        price = black_scholes_price(
            S0, payload.K, payload.r, payload.sigma, payload.T, payload.type
        )
        meta = {"source": "black_scholes"}
    else:
        price, meta = quantum_price_stub(
            S0, payload.K, payload.r, payload.sigma, payload.T, payload.type
        )

    resp = OptionPriceResponse(
        ticker=payload.ticker,
        method=payload.method,
        type=payload.type,
        S0=S0,
        K=payload.K,
        r=payload.r,
        sigma=payload.sigma,
        T=payload.T,
        price=float(price),
        meta=meta,
    )

    return jsonify(resp.model_dump())


@bp.route("/price/option/european/qe/call", methods=["POST"])
def price_option_european_qe_call():
    return (
        jsonify(
            {"message": "Quantum European Call Option pricing is not yet implemented."}
        ),
        501,
    )


@bp.route("/price/option/european/qe/put", methods=["POST"])
def price_option_european_qe_put():
    return (
        jsonify(
            {"message": "Quantum European Put Option pricing is not yet implemented."}
        ),
        501,
    )


@bp.route("/price/option/european/qe", methods=["POST"])
def price_option_european_qe():
    return (
        jsonify({"message": "Quantum European Option pricing is not yet implemented."}),
        501,
    )
