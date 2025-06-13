class Turntable:
    """
    Singleton class representing a turntable with adjustable rotations per minute (RPM).

    This class ensures only one instance exists and provides an attribute to store the current RPM.
    """

    _instance: 'Turntable' = None

    def __new__(cls) -> 'Turntable':
        """
        Create or return the singleton instance of Turntable.

        :param cls: The class type.
        :type cls: type
        :return: The singleton instance of Turntable.
        :rtype: Turntable
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Turntable instance.

        Sets the rotations per minute (RPM) to 0.0.
        """
        self.rotations_per_minute: float = 0.0
