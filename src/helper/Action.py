from enum import Enum


class Action(Enum):
    """
    Enumeration representing possible actions for a system.

    Actions include starting, stopping, pausing, resuming, turning off,
    opening the door, and closing the door.
    """

    START = "START"
    STOP = "STOP"
    PAUSE = "PAUSE"
    RESUME = "RESUME"
    OFF = "OFF"
    OPEN_DOOR = "OPEN_DOOR"
    CLOSE_DOOR = "CLOSE_DOOR"

    def __eq__(self, other: object) -> bool:
        """
        Compare this Action with another object for equality.

        :param other: The object to compare with. Can be a string or another Action.
        :type other: object
        :return: True if the other object is a string equal to this Action's value,
                 or if it is an Action with the same value; otherwise, False.
        :rtype: bool
        """
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
