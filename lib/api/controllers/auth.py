from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token

from lib.db.schemas import user_schema
from extensions import db
from lib.db.models import User
from lib.api.controllers.exceptions import ResourceNotFoundError, AuthenticationFailedError

auth_bp = Blueprint("authentication", __name__)

@auth_bp.route("/register", methods=["POST"])
def add_new_user():
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    new_user = user_schema.load({"name": name, "email": email, "password": password})
    
    db.session.add(new_user)
    db.session.commit()

    return {"user": user_schema.dump(new_user)}, 201


@auth_bp.post("/login")
def login_user():
    email = request.get_json()["email"]
    password = request.get_json()["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        raise ResourceNotFoundError
    
    if not user.check_password(password):
        raise AuthenticationFailedError
   
    
    return jsonify({"user": {"id": user.id, "name": user.name, "email": user.email}, 
                    "access_token": create_access_token(identity=user.id)}), 200