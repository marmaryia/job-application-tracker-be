class CustomException(Exception):
    pass

class ResourceNotFoundError(CustomException):
    status_code = 404
    message = "Resource not found"

class AuthenticationFailedError(CustomException):
    status_code = 401
    message = "Authentication Failed"

class AccessDeniedError(CustomException):
    status_code = 403
    message = "Unauthorised"

class DuplicateResourceError(CustomException):
    error_code = "DUPLICATE_RESOURCE"
    status_code = 400
    message = "This resource already exists"

    def __init__(self, *duplicates):
        self.duplicates = duplicates[0] if len(duplicates) else None

class InvalidQueryError(CustomException):
    status_code = 400
    message = "Bad Request"

class ActionForbiddenError(CustomException):
    status_code = 400
    message = "This action is not allowed"
    error_code = "FORBIDDEN_ACTION"