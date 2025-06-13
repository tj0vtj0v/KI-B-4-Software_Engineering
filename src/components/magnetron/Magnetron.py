class Magnetron:
    """
    Singleton class representing a Magnetron device with basic on/off functionality.

    This class ensures only one instance exists and provides methods to control the device's state.
    """

    _instance: "Magnetron" = None

    def __new__(cls, *args, **kwargs) -> "Magnetron":
        """
        Create or return the singleton instance of Magnetron.

        :param args: Positional arguments (unused).
        :param kwargs: Keyword arguments (unused).
        :return: The singleton instance of Magnetron.
        """
        if cls._instance is None:
            cls._instance = super(Magnetron, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Magnetron instance.

        Sets the initial state of the device to inactive.
        """
        self.active: bool = False

    def turn_on(self) -> None:
        """
        Activate the Magnetron device.

        :return: None
        """
        self.active = True

    def turn_off(self) -> None:
        """
        Deactivate the Magnetron device.

        :return: None
        """
        self.active = False
