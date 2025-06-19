from os import environ
from datetime import timedelta

SQLALCHEMY_DATABASE_URI="sqlite:///tracker.db"
JWT_SECRET_KEY=environ.get("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)