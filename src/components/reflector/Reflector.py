class Reflector:
    """
    Singleton class representing a reflector with an adjustable angle.

    This class ensures only one instance exists and provides an interface
    to manage the reflector's angle.
    """

    _instance: 'Reflector' = None

    def __new__(cls) -> 'Reflector':
        """
        Create or return the singleton instance of Reflector.

        :param cls: The class type.
        :type cls: type
        :return: The singleton instance of Reflector.
        :rtype: Reflector
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Reflector instance with a default angle of 0.

        :return: None
        """
        self.angle: int = 0
