from extensions import db
from lib.db.models import User, Application, Event
from datetime import datetime

def seed(users, applications, events):
    db.drop_all()
    db.create_all()
    
    new_entries = []
    for user in users:
        new_user = User(name=user["name"], email=user["email"], password=user["password"])
        new_entries.append(new_user)

    for application in applications:
        new_application = Application(user_id=application["user_id"], company=application["company"], position=application["position"], status=application["status"], date_created=datetime.strptime(application["date_created"], '%Y-%m-%d %H:%M:%S'), job_url=application["job_url"], notes=application["notes"])
        new_entries.append(new_application)

    for event in events:
        new_event = Event(user_id=event["user_id"], application_id=event["application_id"], title=event["title"], date=datetime.strptime(event["date"], '%Y-%m-%d %H:%M:%S'), notes=event["notes"])
        new_entries.append(new_event)

    db.session.add_all(new_entries)
    db.session.commit()

    