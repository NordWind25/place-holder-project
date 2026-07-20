class JSONPlaceholderBaseError(Exception):
    pass

class JSONPlaceholderClientError(JSONPlaceholderBaseError):
    pass

class JSONPlaceholderServerError(JSONPlaceholderBaseError):
    pass