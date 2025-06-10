class CustomException(Exception):
    """Base class for custom exceptions."""

    def __init__(self, message):
        super().__init__(message)


class MockException(CustomException):
    """Mock exception for testing purposes."""

    def __init__(self):
        super().__init__("This is a mock exception.")


class DoorException(CustomException):
    """Exception raised for errors related to door operations."""

    def __init__(self, message):
        super().__init__(message)


class ProgramAlreadyRunningException(CustomException):
    """Exception raised when a program is already running."""

    def __init__(self):
        super().__init__("A program is already running.")
