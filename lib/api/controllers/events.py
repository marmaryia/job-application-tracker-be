from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity


from extensions import db 
from lib.db.models import Event
from lib.api.controllers.exceptions import ResourceNotFoundError
from lib.utils.identity_check import identity_check

events_bp = Blueprint("events", __name__)

@events_bp.delete("/events/<int:event_id>")
@jwt_required()
def delete_event(event_id):
    identity = get_jwt_identity()
    event = Event.query.filter_by(event_id=event_id).first()
    
    if not event:
        raise ResourceNotFoundError
    
    identity_check(identity, event.user_id)
    
    db.session.delete(event)
    db.session.commit()
    
    return {}, 204