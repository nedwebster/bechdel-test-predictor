class MovieNotFoundError(Exception):
    def __init__(self, title):
        message = f"Movie '{title}' was not found :("
        super().__init__(message)
