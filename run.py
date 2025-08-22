from app import create_app

app = create_app()

if __name__ == "__main__":
    # For local dev only; use gunicorn in production
    app.run(host="0.0.0.0", port=8000, debug=app.config.get("DEBUG", False))