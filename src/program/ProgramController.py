import threading

from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel
from src.program.Program import Program


class ProgramController:
    """
    Singleton controller class to manage the lifecycle of a `Program` instance.
    Provides methods to start, pause, resume, stop, and query the state of the program.
    """

    _instance: 'ProgramController' = None

    def __new__(cls, *args, **kwargs) -> 'ProgramController':
        """
        Ensures only one instance of ProgramController exists (Singleton pattern).

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The singleton instance of ProgramController.
        """
        if cls._instance is None:
            cls._instance = super(ProgramController, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the ProgramController with a logger and sets initial state.
        """
        self.logger: Logger = Logger("ProgramControl")
        self.program: Program | None = None
        self.thread: threading.Thread | None = None

    def start(self, program: Program) -> None:
        """
        Starts the given program in a new thread.

        :param program: The Program instance to start.
        :return: None
        """
        self.logger.log(f"Starting program: {program.get_name()}", LogLevel.INFO)
        self.program = program
        self.thread = threading.Thread(target=self.program.start, name="ProgramThread")
        self.thread.start()

    def pause(self) -> None:
        """
        Pauses the currently running program.

        :return: None
        """
        self.logger.log(f"Pausing program: {self.program.name}", LogLevel.INFO)
        self.program.pause()

    def resume(self) -> None:
        """
        Resumes the currently paused program.

        :return: None
        """
        self.logger.log(f"Resuming program: {self.program.name}", LogLevel.INFO)
        self.program.resume()

    def stop(self) -> None:
        """
        Stops the currently running program and waits for its thread to finish.

        :return: None
        """
        if self.program is None:
            self.logger.log("No program to stop", LogLevel.WARNING)
            return

        self.logger.log(f"Stopping program: {self.program.name}", LogLevel.INFO)
        self.program.stop()

        if self.thread:
            self.thread.join()

    def emergency_stop(self) -> None:
        """
        Immediately stops the currently running program and waits for its thread to finish.

        :return: None
        """
        self.logger.log(f"Emergency stopping program: {self.program.name}", LogLevel.INFO)
        self.program.emergency_stop()

        if self.thread:
            self.thread.join()

    def is_running(self) -> bool:
        """
        Checks if the program is currently running.

        :return: True if the program is running, False otherwise.
        """
        if self.program is None:
            return False

        return self.program.running

    def is_finished(self) -> bool:
        """
        Checks if the program has finished execution.

        :return: True if the program is finished or not set, False otherwise.
        """
        if self.program is None:
            return True

        return self.program.finished

    def is_paused(self) -> bool:
        """
        Checks if the program is currently paused.

        :return: True if the program is paused, False otherwise.
        """
        if self.program is None:
            return False

        return self.program.paused

    def get_running_program(self) -> str:
        """
        Gets the name of the currently running program.

        :return: The name of the running program, or a message if none is running.
        """
        if self.program is None:
            return "No program running"

        return self.program.get_name()

    def get_state_tuple(self) -> tuple[str, bool, bool, bool]:
        """
        Returns a tuple representing the current program state.

        :return: Tuple of (program name, is running, is finished, is paused).
        """
        return self.get_running_program(), self.is_running(), self.is_finished(), self.is_paused()
