from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("lib/config.py")

    db.init_app(app)
    ma.init_app(app)

    from lib.db.models import  User, Application, Event

    from lib.api.routes.routes import api_bp
    app.register_blueprint(api_bp, url_prefix ="/api")

    migrate = Migrate(app, db)

    return app







