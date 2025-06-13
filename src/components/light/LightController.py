import threading
import time

from src.components.door.Door import Door
from src.components.light.Light import Light
from src.helper.Logger import Logger
from src.helper.config import LIGHT_UPDATE_INTERVAL_IN_SECONDS
from src.helper.logging.LogLevel import LogLevel
from src.program.ProgramController import ProgramController


class LightController:
    """
    Singleton controller for managing the light based on door and program state.
    """

    _instance: 'LightController' = None

    def __new__(cls) -> 'LightController':
        """
        Create or return the singleton instance of LightController.

        :return: The singleton instance of LightController.
        :rtype: LightController
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the LightController, setting up logger, light, door, and program controller.
        """
        self.logger: Logger = Logger("LightControl")
        self.light: Light = Light()
        self.door: Door = Door()
        self.program: ProgramController = ProgramController()
        self.running: bool = False
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        """
        Start the light control loop in a separate thread if not already running.

        :return: None
        """
        if not self.running:
            self.logger.log("Starting light control", LogLevel.INFO)
            self.running = True
            self.thread = threading.Thread(target=self.light_loop, name="LightThread")
            self.thread.start()
        else:
            self.logger.log("Light control is already running", LogLevel.WARNING)

    def stop(self) -> None:
        """
        Stop the light control loop and wait for the thread to finish.

        :return: None
        """
        if self.running:
            self.logger.log("Stopping light control", LogLevel.INFO)
            self.running = False
            if self.thread:
                self.thread.join()
        else:
            self.logger.log("Light control is not running", LogLevel.WARNING)

    def light_cycle(self) -> None:
        """
        Update the light state based on the door and program status.

        :return: None
        """
        program_condition: bool = self.program.is_running() and not (
                    self.program.is_paused() or self.program.is_finished())

        if self.door.opened or program_condition:
            if not self.light.on:
                self.light.on = True
                self.logger.log("Light turned on", LogLevel.INFO)
        else:
            if self.light.on:
                self.light.on = False
                self.logger.log("Light turned off", LogLevel.INFO)

    def light_loop(self) -> None:
        """
        Continuously run the light cycle at a fixed interval while running.

        :return: None
        """
        while self.running:
            self.light_cycle()
            time.sleep(LIGHT_UPDATE_INTERVAL_IN_SECONDS)
