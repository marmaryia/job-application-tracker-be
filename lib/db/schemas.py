from extensions import ma
from lib.db.models import User, Application, Event
from marshmallow import fields, validate


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Email(error="Email address not valid") )
    password = fields.Str(required=True, load_only=True, validate=validate.And(validate.Length(min=8, error="Invalid password"), validate.ContainsNoneOf(" ", error="Invalid password")))
    

user_schema = UserSchema()
users_schema = UserSchema(many= True)

class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = True
        
    user_id = fields.Int()
    application_id = fields.Int(dump_only=True)
    events = fields.Nested("EventSchema", many = True, exclude=("application_id", "user_id"), dump_only=True)
    latest_event = fields.Nested("EventSchema", exclude=("application_id", "user_id", "notes"), dump_only=True)


    
applications_schema = ApplicationSchema(many=True, exclude=("events", "notes", "user_id"))
application_schema = ApplicationSchema(exclude=["latest_event"])

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event

    user_id = ma.auto_field()
    application_id = ma.auto_field()



event_schema = EventSchema()
events_schema = EventSchema(many=True)