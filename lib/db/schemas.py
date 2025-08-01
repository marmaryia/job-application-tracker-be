from extensions import ma
from lib.db.models import User, Application, Event
from marshmallow import fields, validate, validates_schema, ValidationError
from datetime import datetime, timezone

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Str(required=True, validate=validate.Email(error="Email address not valid") )
    password = fields.Str(required=True, load_only=True, validate=validate.And(validate.Length(min=8, error="Invalid password"), validate.ContainsNoneOf(" ", error="Invalid password")))
    

user_schema = UserSchema()
users_schema = UserSchema(many= True)

class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = True
        
    user_id = fields.Int(load_only=True)
    application_id = fields.Int(dump_only=True)
    company = fields.String(validate=validate.Length(min=1))
    position = fields.String(validate=validate.Length(min=1))
    events = fields.Nested("EventSchema", many = True, exclude=("application_id", "user_id"), dump_only=True)
    latest_event = fields.Nested("EventSchema", exclude=("application_id", "user_id", "notes"), dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        
        if data["date_created"].replace(tzinfo=timezone.utc) > datetime.now(tz=timezone.utc):
            raise ValidationError("Dates in the future are not allowed")


applications_schema = ApplicationSchema(many=True, exclude=("events", "notes", "user_id"))
application_schema = ApplicationSchema(exclude=["latest_event"])
applications_schema_partial = ApplicationSchema(only=["application_id", "position", "company", "date_created"])

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True

    user_id = ma.auto_field()
    application_id = ma.auto_field()
    event_id = ma.auto_field(dump_only=True)
    title = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data["date"].replace(tzinfo=timezone.utc) > datetime.now(tz=timezone.utc):
            raise ValidationError("Dates in the future are not allowed")



event_schema = EventSchema()
events_schema = EventSchema(many=True)