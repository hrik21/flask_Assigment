from application.configs.db import DbDevelopmentConfig
from application.configs.environ import EnvironConfig

#print(DbDevelopmentConfig.DB_CONNECTION_STRING,)
#print(EnvironConfig.APP_ENVIRONMENT)
#print(EnvironConfig.FLASK_APP_SECRET)

class Config:
    SQLALCHEMY_DATABASE_URI = DbDevelopmentConfig.DB_CONNECTION_STRING
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY=EnvironConfig.FLASK_APP_SECRET