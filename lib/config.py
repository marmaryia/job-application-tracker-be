from os import environ

SQLALCHEMY_DATABASE_URI="sqlite:///tracker.db"
JWT_SECRET_KEY=environ.get("JWT_SECRET_KEY")