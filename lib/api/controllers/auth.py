from flask import request, jsonify, Blueprint
from lib.db.models import User
from lib.db.schemas import user_schema

from app import db

auth_bp = Blueprint("authentication", __name__)


@auth_bp.route("/add_new_user", methods=["POST"])
def add_new_user():
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    print(name, email, password)
    new_user = user_schema.load({"name": name, "email": email, "password": password})
    
    db.session.add(new_user)
    db.session.commit()

    return {"user": user_schema.dump(new_user)}