from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("lib/config.py")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    from lib.db.models import  User, Application, Event

    from lib.api.routes.routes import api_bp
    from lib.api.controllers.auth import auth_bp
    app.register_blueprint(api_bp, url_prefix ="/api")
    app.register_blueprint(auth_bp, url_prefix ="/api/users")

    migrate.init_app(app, db)

    return app







