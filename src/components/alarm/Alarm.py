class Alarm:
    """
    Singleton class representing an alarm system.

    Ensures only one instance of the Alarm class exists.
    """

    _instance: 'Alarm' = None

    def __new__(cls, *args: object, **kwargs: object) -> 'Alarm':
        """
        Create or return the singleton instance of Alarm.

        :param args: Positional arguments (unused).
        :param kwargs: Keyword arguments (unused).
        :return: The singleton instance of Alarm.
        """
        if cls._instance is None:
            cls._instance = super(Alarm, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Alarm instance.

        Sets the alarm to inactive by default.
        """
        self.active: bool = False
