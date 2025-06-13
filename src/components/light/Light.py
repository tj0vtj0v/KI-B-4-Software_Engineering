class Light:
    """
    Singleton class representing a light component.

    This class ensures only one instance of Light exists.
    """

    _instance: 'Light' = None

    def __new__(cls) -> 'Light':
        """
        Create or return the singleton instance of Light.

        :param cls: The class type.
        :type cls: type
        :return: The singleton instance of Light.
        :rtype: Light
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Light instance.

        Sets the light state to off.
        """
        self.on: bool = False
