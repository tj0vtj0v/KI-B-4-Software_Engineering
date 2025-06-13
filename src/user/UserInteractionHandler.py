from src.components.door.Door import Door
from src.helper.Action import Action
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel
from src.program.DefrostingProgram import DefrostingProgram
from src.program.Program import Program
from src.user.InputDetector import InputDetector


class UserInteractionHandler:
    """
    Singleton class responsible for handling user interactions, such as detecting actions and managing the door state.
    """

    _instance: "UserInteractionHandler" = None

    def __new__(cls) -> "UserInteractionHandler":
        """
        Ensures only one instance of UserInteractionHandler exists.

        :return: The singleton instance of UserInteractionHandler.
        :rtype: UserInteractionHandler
        """
        if cls._instance is None:
            cls._instance = super(UserInteractionHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the UserInteractionHandler, setting up the logger, door, and input detector.
        """
        self.logger: Logger = Logger("UserInteraction")
        self.door: Door = Door()
        self.input_detector: InputDetector = InputDetector()
        self.input_detector.start()

    def get_interactions(self) -> tuple[Action | None, Program | None]:
        """
        Retrieves the latest user action and processes it accordingly.

        :return: A tuple containing the detected Action (or None) and the corresponding Program (or None).
        :rtype: tuple[Action | None, Program | None]
        """
        action: Action | None = self.input_detector.get_latest_action()

        match action:
            case Action.START:
                self.logger.log("User requested to start a program", LogLevel.INFO)
                return action, DefrostingProgram()

            case Action.OPEN_DOOR:
                if not self.door.opened:
                    self.logger.log("User opened the door", LogLevel.INFO)
                    self.door.open()
                return None, None

            case Action.CLOSE_DOOR:
                if self.door.opened:
                    self.logger.log("User closed the door", LogLevel.INFO)
                    self.door.close()
                return None, None

            case _:  # stop pause resume off
                return action, None
        return None, None

    def update_display(self, program_name: str, running: bool, finished: bool, paused: bool) -> None:
        """
        Updates the display with the current program status.

        :param program_name: The name of the current program.
        :type program_name: str
        :param running: Indicates if the program is currently running.
        :type running: bool
        :param finished: Indicates if the program has finished.
        :type finished: bool
        :param paused: Indicates if the program is paused.
        :type paused: bool
        :return: None
        """
        pass
