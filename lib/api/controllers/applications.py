from flask import Blueprint, request
from sqlalchemy import asc, desc
from sqlalchemy.sql import func
from flask_jwt_extended import jwt_required, get_jwt_identity

from lib.db.models import Application, Event, User
from lib.db.schemas import applications_schema, application_schema
from lib.api.controllers.exceptions import ResourceNotFoundError, InvalidQueryError, AccessDeniedError
from lib.utils.identity_check import identity_check
from extensions import db

applications_bp = Blueprint("applications", __name__)

@applications_bp.get("/users/<int:user_id>/applications")
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

@applications_bp.patch("/applications/<int:application_id>")
@jwt_required()
def patch_application_status(application_id):
    identity = get_jwt_identity()
    application = Application.query.filter_by(application_id=application_id).first()
    
    if not application:
        raise ResourceNotFoundError
    
    identity_check(identity, application.user_id)
    
    new_status = request.get_json()["new_status"]
    
    if new_status == application.status:
        raise InvalidQueryError

    application.status = new_status

    new_event = Event(user_id=application.user_id, application_id=application.application_id, title=f"Status change to {new_status}")
    db.session.add(new_event)
    db.session.commit()
    
    return {"application": application_schema.dump(application)}, 200