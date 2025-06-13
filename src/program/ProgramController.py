import threading

from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel
from src.program.Program import Program


class ProgramController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProgramController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("ProgramControl")

        self.program = None
        self.thread = None

    def start(self, program: Program):
        self.logger.log(f"Starting program: {program.get_name()}", LogLevel.INFO)

        self.program = program

        self.thread = threading.Thread(target=self.program.start, name="ProgramThread")
        self.thread.start()

    def pause(self):
        self.logger.log(f"Pausing program: {self.program.name}", LogLevel.INFO)
        self.program.pause()

    def resume(self):
        self.logger.log(f"Resuming program: {self.program.name}", LogLevel.INFO)
        self.program.resume()

    def stop(self):
        if self.program is None:
            self.logger.log("No program to stop", LogLevel.WARNING)
            return

        self.logger.log(f"Stopping program: {self.program.name}", LogLevel.INFO)
        self.program.stop()

        if self.thread:
            self.thread.join()

    def emergency_stop(self):
        self.logger.log(f"Emergency stopping program: {self.program.name}", LogLevel.INFO)
        self.program.emergency_stop()

        if self.thread:
            self.thread.join()

    def is_running(self):
        if self.program is None:
            return False

        return self.program.running

    def is_finished(self):
        if self.program is None:
            return True

        return self.program.finished

    def is_paused(self):
        if self.program is None:
            return False

        return self.program.paused

    def get_running_program(self):
        if self.program is None:
            return "No program running"

        return self.program.get_name()

    def get_state_tuple(self) -> tuple[str, bool, bool, bool]:
        return self.get_running_program(), self.is_running(), self.is_finished(), self.is_paused()
