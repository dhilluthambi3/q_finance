import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = bool(int(os.getenv("FLASK_DEBUG", "0")))
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # Rate limiting
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "120/minute")

    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI")


    # Redis / Mongo
    REDIS_URL = os.getenv("REDIS_URL")
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DB = os.getenv("MONGODB_DB", "finance_api")

    # App meta
    APP_NAME = os.getenv("APP_NAME", "finance-api")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
