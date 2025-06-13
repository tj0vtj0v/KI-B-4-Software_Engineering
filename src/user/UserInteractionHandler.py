from src.components.door.Door import Door
from src.helper.Action import Action
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel
from src.program.DefrostingProgram import DefrostingProgram
from src.program.Program import Program
from src.user.InputDetector import InputDetector


class UserInteractionHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserInteractionHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("UserInteraction")

        self.door = Door()
        self.input_detector = InputDetector()
        self.input_detector.start()

    def get_interactions(self) -> tuple[Action | None, Program | None]:
        action = self.input_detector.get_latest_action()

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

    def update_display(self, program_name: str, running: bool, finished: bool, paused: bool):
        pass
