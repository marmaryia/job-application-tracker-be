from flask import Blueprint, request
from sqlalchemy import asc, desc

from extensions import db
from lib.db.models import Application, Event, User
from lib.db.schemas import applications_schema
from lib.api.controllers.exceptions import ResourceNotFoundError

applications_bp = Blueprint("applications", __name__)

@applications_bp.get("/<int:user_id>/applications")
def get_applications_by_user_id(user_id):
    
    if not User.query.filter_by(id=user_id).first():
        raise ResourceNotFoundError

    order = request.args.get("order", "desc")
    sort_by = request.args.get("sort_by", "date_created")

    allowed_columns = {
        "date_created": Application.date_created,
        "recent_activity": Event.date,
    }

    order_column = allowed_columns.get(sort_by)

    ordering = asc(order_column) if order == "asc" else desc(order_column)

    query = Application.query.filter_by(user_id=user_id)

    if sort_by == "recent_activity":
        query = query.join(Application.events)

    query = query.order_by(ordering)

    applications_list = query.all()

    return {"applications": applications_schema.dump(applications_list, many=True)}, 200