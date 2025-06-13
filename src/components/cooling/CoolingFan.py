class CoolingFan:
    """
    Singleton class representing a cooling fan component.

    This class ensures only one instance of CoolingFan exists.
    """

    _instance: "CoolingFan" = None

    def __new__(cls) -> "CoolingFan":
        """
        Create or return the singleton instance of CoolingFan.

        :param cls: The class type.
        :type cls: type
        :return: The singleton instance of CoolingFan.
        :rtype: CoolingFan
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the CoolingFan instance.

        Sets the initial power_share to 0.0.
        """
        self.power_share: float = 0.0
