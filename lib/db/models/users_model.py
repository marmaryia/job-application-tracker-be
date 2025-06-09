from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app import db, ma


print("users loaded")
class User(db.Model):
    __tablename__ = "users" 
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)
    #applications = relationship("Application", uselist=True,back_populates="user")

    def __repr__(self):
        return f"User with id {self.id}, email {self.email}"
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    email = ma.auto_field()
    name = ma.auto_field()


user_schema = UserSchema()
users_schema = UserSchema(many= True)