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
    
    from lib.db.models.users_model import User
    from lib.db.models.applications_model import Application
    from lib.db.models.events_model import Event
    
    from lib.api.routes.routes import api_bp
    app.register_blueprint(api_bp, url_prefix ="/api")

    migrate = Migrate(app, db, render_as_batch=True)

    return app







