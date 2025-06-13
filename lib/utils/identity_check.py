from lib.api.controllers.exceptions import AccessDeniedError

def identity_check(identity, id):
    if identity != str(id):
        raise AccessDeniedError