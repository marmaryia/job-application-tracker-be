from app import ma
from lib.db.models import User, Application, Event
from marshmallow_sqlalchemy import fields 


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    email = ma.auto_field()
    name = ma.auto_field()
    applications = fields.Nested("ApplicationSchema", many=True)


user_schema = UserSchema()
users_schema = UserSchema(many= True)

class ApplicationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Application
    
    application_id = ma.auto_field()
    user_id = ma.auto_field()
    company = ma.auto_field()
    position = ma.auto_field()
    status = ma.auto_field() 
    date_created = ma.auto_field()
    job_url = ma.auto_field()
    notes = ma.auto_field()
    events = fields.Nested("EventSchema", many=True, exclude=("user_id", "application_id"))
    

application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)


class EventSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Event

    event_id = ma.auto_field()
    user_id = ma.auto_field()
    application_id = ma.auto_field()
    title = ma.auto_field()
    date = ma.auto_field()
    notes = ma.auto_field()


event_schema = EventSchema()
events_schema = EventSchema(many=True)