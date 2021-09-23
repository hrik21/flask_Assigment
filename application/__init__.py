from application.configs import Config
from application.configs.environ import EnvironConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask



db = SQLAlchemy()


def create_app():
    app =Flask(__name__)
    app.config.from_object(Config)

  
    db.init_app(app)
    Migrate(app,db)

    with app.app_context():

        from application.routes import auth
        app.register_blueprint(auth.auth_bp)
        return app

