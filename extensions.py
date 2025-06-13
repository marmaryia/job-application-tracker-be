from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)