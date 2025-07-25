from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from extensions import db 
from lib.db.models import Event, User, Application
from lib.api.controllers.exceptions import ResourceNotFoundError, ActionForbiddenError
from lib.utils.identity_check import identity_check
from lib.db.schemas import event_schema

events_bp = Blueprint("events", __name__)

@events_bp.delete("/events/<int:event_id>")
@jwt_required()
def delete_event(event_id):
    identity = get_jwt_identity()
    event = Event.query.filter_by(event_id=event_id).first()
    
    if not event:
        raise ResourceNotFoundError
    
    if event.undeletable:
        raise ActionForbiddenError("Deleting forbidden")
    
    identity_check(identity, event.user_id)
    
    db.session.delete(event)
    db.session.commit()
    
    return {}, 204

@events_bp.post("/events")
@jwt_required()
def add_event():

    event_data = request.get_json()
    
    user = User.query.filter_by(id=event_data["user_id"]).first()
    
    if not user:
        raise ResourceNotFoundError
    
    identity = get_jwt_identity()
    identity_check(identity, event_data["user_id"])

    if "application_id" in event_data:
        application = Application.query.filter_by(application_id = event_data["application_id"], user_id = event_data["user_id"]).first()
        if not application:
            raise ResourceNotFoundError
        
        if datetime.strptime(event_data["date"], "%Y-%m-%dT%H:%M:%S")  < application.date_created:
            raise ActionForbiddenError("Date out of sequence")

    

    new_event = event_schema.load(event_data)
    
    db.session.add(new_event)

    db.session.commit()
 
    return {"event": event_schema.dump(new_event)}, 201