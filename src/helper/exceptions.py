class CustomException(Exception):
    """Base class for custom exceptions."""

    def __init__(self, message):
        super().__init__(message)


class MockException(CustomException):
    """Mock exception for testing purposes."""

    def __init__(self):
        super().__init__("This is a mock exception.")
