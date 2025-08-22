import pytest

from lib.db.seed import seed
from extensions import db
from lib.db.data import users, applications, events
from lib.db.models import User, Application, Event
from app import create_app

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    yield app

def test_seed(app):
    with app.app_context():
        seed(users, applications, events)

        users_from_db = db.session.query(User).all()
        assert len(users_from_db) == 4
        for user in users_from_db:
            assert user.id in [1, 2, 3, 4]

        applications_from_db = db.session.query(Application).all()
        assert len(applications_from_db) == 10
        for application in applications_from_db:
            assert application.user_id in [1, 2, 3]
            assert isinstance(application.user, User)
            for event in application.events:
                assert isinstance(event, Event)
            assert isinstance(application.latest_event, Event) or application.latest_event == None

        events_from_db = db.session.query(Event).all()
        assert len(events_from_db) == 20
        for event in events_from_db:
            assert event.user_id in [1, 2, 3]