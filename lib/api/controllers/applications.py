from flask import Blueprint, request
from sqlalchemy import asc, desc, or_
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from dateutil.parser import parse

from lib.db.models import Application, Event, User
from lib.db.schemas import applications_schema, application_schema, applications_schema_partial
from lib.api.controllers.exceptions import ResourceNotFoundError, InvalidQueryError, DuplicateResourceError
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
    search = request.args.get("search")

    allowed_sort_columns = {
        "date_created": Application.date_created,
        "recent_activity": Event.date,
    }

    order_column = allowed_sort_columns.get(sort_by)

    ordering = asc(order_column) if order == "asc" else desc(order_column)

    query = Application.query.filter_by(user_id=user_id)
    
    if search:
        query = query.filter(or_(Application.company.ilike(f"%{search}%"), Application.position.ilike(f"%{search}%")))

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

@applications_bp.post("/applications")
@jwt_required()
def add_new_application():
    body = request.get_json()
    data = {k: v for k, v in body.items() if k != "allow_duplicates"}
    user = User.query.filter_by(id=data["user_id"]).first()
    allow_duplicates = body["allow_duplicates"] if "allow_duplicates" in body else False

    if not user:
        raise ResourceNotFoundError
    
    identity = get_jwt_identity()
    identity_check(identity, data["user_id"])

    if not allow_duplicates and "job_url" in data and data["job_url"]:
        duplicate_applications = db.session.query(Application).filter_by(job_url=data["job_url"], user_id=data["user_id"]).all()
        if len(duplicate_applications) != 0:
            duplicate_url_applications = applications_schema_partial.dump(duplicate_applications, many=True)
            raise DuplicateResourceError(duplicate_url_applications)

    new_application = application_schema.load(data)
    db.session.add(new_application)
    db.session.commit()

    event_title = "Application created"
    if new_application.status != "Application sent":
        event_title += f" with status {new_application.status}"

    new_event = Event(user_id=data["user_id"], application_id=new_application.application_id, title=event_title, date=new_application.date_created, undeletable=True)
    
    db.session.add(new_event)
    db.session.commit()

    return {"application": application_schema.dump(new_application)}, 201


@applications_bp.delete("/applications/<int:application_id>")
@jwt_required()
def delete_application(application_id):
    identity = get_jwt_identity()
    application = Application.query.filter_by(application_id=application_id).first()
    
    if not application:
        raise ResourceNotFoundError
    
    identity_check(identity, application.user_id)
    
    db.session.delete(application)
    db.session.commit()
    
    return {}, 204

@applications_bp.get("/applications/<int:application_id>")
@jwt_required()
def get_application_by_id(application_id):
    identity = get_jwt_identity()
    application = db.session.query(Application).filter_by(application_id=application_id).first()
    
    if not application:
        raise ResourceNotFoundError
    
    identity_check(identity, application.user_id)

    return {"application": application_schema.dump(application)}, 200

@applications_bp.put("/applications/<int:application_id>")
@jwt_required()
def update_application_by_id(application_id):
    identity = get_jwt_identity()
    application = db.session.query(Application).filter_by(application_id=application_id).first()
    
    if not application:
        raise ResourceNotFoundError
    
    identity_check(identity, application.user_id)

    new_data = request.get_json()
    new_data["notes"] = new_data["notes"] if "notes" in new_data else None 
    new_data["job_url"] = new_data["job_url"] if "job_url" in new_data else None 
    new_data["date_created"] = parse(new_data["date_created"])
    
    updated_fields = []
    
    for field, value in new_data.items():
        if getattr(application, field) != value:
            setattr(application, field, value)
            updated_fields.append(field)

    if "date_created" in updated_fields:
        application.events.order_by(Event.date.asc()).first().date = new_data["date_created"]
        application.events = [event for event in application.events if event.date >= new_data["date_created"]]
    
    if len(updated_fields) > 0:
        event_notes = "Updated fields:"
        for field in updated_fields:
            event_notes += f" {field},"
        event_notes = event_notes[:len(event_notes) - 1]
        new_event = Event(user_id=application.user_id, application_id=application.application_id, title=f"Information updated", notes=event_notes)
        db.session.add(new_event)

    db.session.commit()

    return {"application": application_schema.dump(application)}, 201