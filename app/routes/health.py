from flask import Blueprint, jsonify, current_app, request

bp = Blueprint("health", __name__)


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "app": current_app.config.get("APP_NAME"),
        "version": current_app.config.get("APP_VERSION"),
        "request_id": request.headers.get("X-Request-Id"),
    })