from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import datetime, timezone

from lib.db.schemas import user_schema
from extensions import db, jwt
from lib.db.models import User, TokenBlocklist
from lib.api.controllers.exceptions import ResourceNotFoundError, AuthenticationFailedError, DuplicateResourceError, InvalidQueryError

@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

auth_bp = Blueprint("authentication", __name__)

@auth_bp.route("/register", methods=["POST"])
def add_new_user():
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    existing_user = User.query.filter_by(email = email).first()

    if existing_user:
        raise DuplicateResourceError

    new_user = user_schema.load({"name": name, "email": email, "password": password})
    
    db.session.add(new_user)
    db.session.commit()

    return {"user": user_schema.dump(new_user)}, 201


@auth_bp.post("/login")
def login_user():
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    if not email or not password:
        raise InvalidQueryError

    user = User.query.filter_by(email=email).first()

    if not user:
        raise ResourceNotFoundError
    
    if not user.check_password(password):
        raise AuthenticationFailedError
   
    return jsonify({"user": user_schema.dump(user), 
                    "access_token": create_access_token(identity=user)}), 200

@auth_bp.delete("/logout")
@jwt_required()
def revoke_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify(message = "Logged out successfully")