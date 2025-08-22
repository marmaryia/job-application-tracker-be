from dateutil.parser import parse

def sort_list_by_date(application):
    return parse(application["date_created"])

def sort_list_by_activity(application):
    return parse(application["latest_event"]["date"])

def create_dummy_user_token(dummy_id):
    class Dummy:
        def __init__(self, id):
            self.id = id 
    dummy_user = Dummy(dummy_id)
    from flask_jwt_extended import create_access_token
    from app import create_app

    app = create_app()
    with app.app_context():
        token = create_access_token(identity=dummy_user)
    return {"Authorization": f"Bearer {token}"}