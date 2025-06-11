from flask import Flask
from marshmallow import ValidationError

from extensions import db, ma, migrate, bcrypt
from lib.api.controllers.error_handlers import handle_exceptions, handle_validation_error, handle_server_errors, handle_custom_exceptions
from lib.api.controllers.exceptions import ResourceNotFoundError


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
    app.register_blueprint(auth_bp, url_prefix ="/api/auth")

    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(Exception, handle_exceptions)
    app.register_error_handler(ResourceNotFoundError, handle_custom_exceptions)
    app.register_error_handler(500, handle_server_errors)

    migrate.init_app(app, db)

    return app







