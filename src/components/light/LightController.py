import threading
import time

from src.components.door.Door import Door
from src.components.light.Light import Light
from src.helper.Logger import Logger
from src.helper.config import LIGHT_UPDATE_INTERVAL_IN_SECONDS
from src.helper.logging.LogLevel import LogLevel
from src.program.ProgramController import ProgramController


class LightController:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("LightControl")
        self.light = Light()

        self.door = Door()
        self.program = ProgramController()

        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.logger.log("Starting light control", LogLevel.INFO)
            self.running = True

            self.thread = threading.Thread(target=self.light_loop, name="LightThread")
            self.thread.start()
        else:
            self.logger.log("Light control is already running", LogLevel.WARNING)

    def stop(self):
        if self.running:
            self.logger.log("Stopping light control", LogLevel.INFO)
            self.running = False

            if self.thread:
                self.thread.join()
        else:
            self.logger.log("Light control is not running", LogLevel.WARNING)

    def light_cycle(self):
        program_condition = self.program.is_running() and not (self.program.is_paused() or self.program.is_finished())

        if self.door.opened or program_condition:
            if not self.light.on:
                self.light.on = True
                self.logger.log("Light turned on", LogLevel.INFO)
        else:
            if self.light.on:
                self.light.on = False
                self.logger.log("Light turned off", LogLevel.INFO)

    def light_loop(self):
        while self.running:
            self.light_cycle()

            time.sleep(LIGHT_UPDATE_INTERVAL_IN_SECONDS)
