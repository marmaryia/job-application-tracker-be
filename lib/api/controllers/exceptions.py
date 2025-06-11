class ResourceNotFoundError(Exception):
    status_code = 404
    message = "Resource not found"