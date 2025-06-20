from flask import Blueprint, request
from sqlalchemy import asc, desc
from flask_jwt_extended import jwt_required, get_jwt_identity

from lib.db.models import Application, Event, User
from lib.db.schemas import applications_schema
from lib.api.controllers.exceptions import ResourceNotFoundError, InvalidQueryError, AccessDeniedError
from lib.utils.identity_check import identity_check

applications_bp = Blueprint("applications", __name__)

@applications_bp.get("/<int:user_id>/applications")
@jwt_required()
def get_applications_by_user_id(user_id):
    identity = get_jwt_identity()
    identity_check(identity, user_id)

    if not User.query.filter_by(id=user_id).first():
        raise ResourceNotFoundError

    order = request.args.get("order", "desc")
    sort_by = request.args.get("sort_by", "date_created")
    status = request.args.get("status")

    allowed_sort_columns = {
        "date_created": Application.date_created,
        "recent_activity": Event.date,
    }

    order_column = allowed_sort_columns.get(sort_by)

    ordering = asc(order_column) if order == "asc" else desc(order_column)

    query = Application.query.filter_by(user_id=user_id)

    if sort_by == "recent_activity":
        query = query.join(Application.events)

    if status == "active":        
        query = query.filter(Application.status.in_(["Application sent", "In review", "Offer received"]))
    elif status == "rejected":
        query = query.filter(Application.status == "Rejected")
    elif status == "archived":
        query = query.filter(Application.status.in_(["Archived", "Offer accepted", "Offer declined"]))
    elif status:
        raise InvalidQueryError

    query = query.order_by(ordering)

    applications_list = query.all()

    return {"applications": applications_schema.dump(applications_list, many=True)}, 200