from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app import db, ma

print("applications_model loaded")

class Application(db.Model):
    __tablename__ = "applications" 
    application_id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    #user = relationship("User", back_populates="applications")
    company = mapped_column(String(250), nullable=False)
    position = mapped_column(String(250), nullable=False)
    status = mapped_column(String(250), nullable=False)
    date_created = mapped_column(DateTime, nullable=False, default=func.now())
    job_url = mapped_column(String(2000), nullable=True)
    notes = mapped_column(Text, nullable=True)
   # events = relationship("Event", uselist=True)

    def __repr__(self):
        return f"Application with id {self.appliction_id} by {self.user_id} to company {self.company}"
    
    def __init__(self, user_id, company, position, status, date_created, job_url, notes):
        self.user_id = user_id
        self.company = company
        self.position = position
        self.status = status
        self.date_created = date_created
        self.job_url = job_url
        self.notes = notes

    __table_args__ = (
        db.CheckConstraint(
            status.in_(['Application sent', 'In review', 'Rejected', 'Archived', 'Offer received', 'Offer accepted', 'Offer declined']),
            name='status_check'
        ),
    )


class ApplicationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Application
    
    application_id = ma.auto_field()
    user_id = ma.auto_field()
    #user = ma.Nested(user_schema)
    company = ma.auto_field()
    position = ma.auto_field()
    status = ma.auto_field() 
    date_created = ma.auto_field()
    job_url = ma.auto_field()
    notes = ma.auto_field()

application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many= True)