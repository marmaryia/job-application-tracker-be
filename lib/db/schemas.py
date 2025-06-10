from app import ma
from lib.db.models import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    email = ma.auto_field()
    name = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many= True)

# class ApplicationSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = Application
    
#     application_id = ma.auto_field()
#     user_id = ma.auto_field()
#     #user = ma.Nested(user_schema)
#     company = ma.auto_field()
#     position = ma.auto_field()
#     status = ma.auto_field() 
#     date_created = ma.auto_field()
#     job_url = ma.auto_field()
#     notes = ma.auto_field()

# application_schema = ApplicationSchema()
# applications_schema = ApplicationSchema(many= True)