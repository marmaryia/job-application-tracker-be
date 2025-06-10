from lib.db.seed import seed
from lib.db.data import users, applications, events
from run import app

with app.app_context():
    seed(users, applications, events)