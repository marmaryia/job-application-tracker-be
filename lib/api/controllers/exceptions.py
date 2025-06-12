class CustomException(Exception):
    pass

class ResourceNotFoundError(CustomException):
    status_code = 404
    message = "Resource not found"

class AuthenticationFailedError(CustomException):
    status_code = 401
    message = "Authentication Failed"

class DuplicateResourceError(CustomException):
    status_code = 400
    message = "This resource already exists"