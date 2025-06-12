from flask import Blueprint

from lib.db.models import Application
from lib.db.schemas import applications_schema

applications_bp = Blueprint("applications", __name__)

@applications_bp.get("/<int:user_id>/applications")
def get_applications_by_user_id(user_id):

    applications_list = Application.query.filter_by(user_id=user_id)    

    return {"applications": applications_schema.dump(applications_list, many=True)}, 200