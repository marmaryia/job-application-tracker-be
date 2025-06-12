class ResourceNotFoundError(Exception):
    status_code = 404
    message = "Resource not found"

class AuthenticationFailedError(Exception):
    status_code = 401
    message = "Authentication Failed"