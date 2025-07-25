from sqlalchemy import Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func, asc
from sqlalchemy.orm import relationship, mapped_column, Mapped
from extensions import db, bcrypt
from typing import List




class User(db.Model):
    __tablename__ = "users" 
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String, nullable=False)
    email:Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password:Mapped[str] = mapped_column(String, nullable=False)
    applications:Mapped[List["Application"]] = relationship("Application", back_populates="user")

    def __repr__(self):
        return f"User with id {self.id}, email {self.email}"
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Application(db.Model):
    __tablename__ = "applications" 
    application_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    user:Mapped["User"] = relationship("User", back_populates="applications")
    company:Mapped[str] = mapped_column(String(250), nullable=False)
    position:Mapped[str] = mapped_column(String(250), nullable=False)
    status:Mapped[str] = mapped_column(String(250), nullable=False)
    date_created:Mapped[str] = mapped_column(DateTime, nullable=False, default=func.now())
    job_url:Mapped[str] = mapped_column(String(2000), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    events: Mapped[List["Event"]] = relationship("Event", order_by=lambda: (asc(Event.date), asc(Event.event_id)), lazy="dynamic", cascade="all, delete", back_populates="application")
    
    @property
    def latest_event(self):
        return (db.session.query(Event).filter_by(application_id=self.application_id).order_by(Event.date.desc(), Event.event_id.desc()).first())


    def __repr__(self):
        return f"Application with id {self.application_id} by {self.user_id} to company {self.company}"
    
    def __init__(self, user_id, company, position, status, date_created = func.now(), job_url=None, notes=None ):
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


class Event(db.Model):
    __tablename__ = "events"

    event_id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"), nullable=False)
    application_id:Mapped[int] = mapped_column(Integer, db.ForeignKey("applications.application_id"), nullable=True)
    title:Mapped[str] = mapped_column(String(250), nullable=False)
    date:Mapped[str] = mapped_column(DateTime, nullable=False, default=func.now())
    notes:Mapped[str] = mapped_column(Text, nullable=True)
    undeletable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    application:Mapped["Application"] = relationship("Application", back_populates="events")
    

    def __repr__(self):
        return f"Event with id {self.event_id} by {self.user_id} associated with {self.application_id}, date: {self.date}"
    
    def __init__(self, user_id, title, application_id=None, notes=None, date=func.now(), undeletable=False):
        self.user_id = user_id
        self.application_id = application_id
        self.title = title
        self.date = date 
        self.notes = notes 
        self.undeletable = undeletable

class TokenBlocklist(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    jti:Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    created_at:Mapped[str] = mapped_column(DateTime, nullable=False)