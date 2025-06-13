class CustomException(Exception):
    """
    Base class for custom exceptions in the application.

    :param message: The error message describing the exception.
    :type message: str
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the CustomException.

        :param message: The error message describing the exception.
        :type message: str
        :return: None
        """
        super().__init__(message)


class MockException(CustomException):
    """
    Exception used for testing purposes.

    This exception is intended to be raised in mock scenarios.
    """

    def __init__(self) -> None:
        """
        Initialize the MockException with a default message.

        :return: None
        """
        super().__init__("This is a mock exception.")


class DoorException(CustomException):
    """
    Exception raised for errors related to door operations.

    :param message: The error message describing the door-related error.
    :type message: str
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the DoorException.

        :param message: The error message describing the door-related error.
        :type message: str
        :return: None
        """
        super().__init__(message)


class ProgramAlreadyRunningException(CustomException):
    """
    Exception raised when a program is already running.

    This exception indicates that an attempt was made to start a program
    that is already active.
    """

    def __init__(self) -> None:
        """
        Initialize the ProgramAlreadyRunningException with a default message.

        :return: None
        """
        super().__init__("A program is already running.")
