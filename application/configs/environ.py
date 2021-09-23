import os


class EnvironConfig:
    APP_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "DEVELOPMENT")
    FLASK_APP_SECRET = os.environ.get("FLASK_APP_SECRET", "thisissecrectkey")