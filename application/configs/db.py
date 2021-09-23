import os


class DbDevelopmentConfig:
    DB_URI = "mysql+pymysql://root@localhost/flask"
    DB_CONNECTION_STRING = os.environ.get(
        "DB_CONNECTION_STRING", os.environ.get("SQLALCHEMY_DATABASE_URI", DB_URI)
    )
