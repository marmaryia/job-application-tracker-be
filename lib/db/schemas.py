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