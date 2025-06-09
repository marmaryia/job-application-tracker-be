from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, mapped_column

from app import db, ma


print("events_model loaded")

class Event(db.Model):
    __tablename__ = "events"

    event_id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    application_id = mapped_column(Integer, db.ForeignKey("applications.application_id"), nullable=True)
    title = mapped_column(String(250), nullable=False)
    date = mapped_column(DateTime, nullable=False)
    notes = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"Event with id {self.application_id} by {self.user_id} associated with {self.application_id}"
    
    def __init__(self, user_id, application_id, title, date, notes):
        self.user_id = user_id
        self.application_id = application_id
        self.title = title
        self.date = date
        self.notes = notes