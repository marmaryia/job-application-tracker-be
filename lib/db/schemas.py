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
        exclude = ("user_id", "notes")
    
    events = fields.Nested("EventSchema", many = True)
    latest_event = fields.Nested("EventSchema", exclude=("application_id", "user_id", "notes"))


    
applications_schema = ApplicationSchema(many=True, exclude=["events"])


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