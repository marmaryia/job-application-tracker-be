from flask import request, jsonify, Blueprint
from lib.db.models.users_model import User, users_schema


api_bp = Blueprint("api_blueprint", __name__)


@api_bp.route("/")
def get_all_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))