from flask import Flask, jsonify, request
from flask_cors import CORS
from .config import Config
from .extensions import limiter, mongo, redis_client
from .utils import request_id_middleware


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    # CORS
    CORS(app, resources={r"*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Extensions
    limiter.init_app(app)

    if app.config.get("MONGODB_URI"):
        mongo.init_app(app, uri=app.config["MONGODB_URI"])
    if app.config.get("REDIS_URL"):
        redis_client.init_app(app)

    # Middleware
    app.before_request(request_id_middleware)

    # Blueprints
    from .routes.health import bp as health_bp
    from .routes.market import bp as market_bp
    from .routes.options import bp as options_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(market_bp, url_prefix="/v1")
    app.register_blueprint(options_bp, url_prefix="/v1")

    # Error handlers
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return (
            jsonify(
                {
                    "error": "rate_limited",
                    "detail": str(e.description),
                    "request_id": request.headers.get("X-Request-Id"),
                }
            ),
            429,
        )

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not_found", "detail": "Route not found"}), 404

    @app.errorhandler(Exception)
    def internal_error(e):
        app.logger.exception("Unhandled error")
        return jsonify({"error": "internal_server_error", "detail": str(e)}), 500

    return app
