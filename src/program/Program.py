import threading
import time
from abc import ABC, abstractmethod

from src.components.cooling.CoolingFanController import CoolingFanController
from src.components.door.DoorController import DoorController
from src.components.magnetron.MagnetronModulator import MagnetronModulator
from src.components.reflector.ReflectorController import ReflectorController
from src.components.sensor.SensorManager import SensorManager
from src.components.turntable.TurntableController import TurntableController
from src.helper.Logger import Logger
from src.helper.config import PROGRAM_UPDATE_INTERVAL_IN_SECONDS
from src.helper.logging.LogLevel import LogLevel


class Program(ABC):
    """
    Abstract base class for a program.
    """
    pause_condition = threading.Condition()

    logger = Logger("ProgramControl")
    sensors = SensorManager()
    door = DoorController()

    magnetron = MagnetronModulator()
    cooling_fan = CoolingFanController()
    turntable = TurntableController()
    reflector = ReflectorController()

    components = [magnetron, cooling_fan, turntable, reflector]

    def __init__(self):
        """
        Defines instance variables
        """
        self.name: str = "Program"
        self.paused: bool = False
        self.running: bool = False
        self.finished: bool = False

    @abstractmethod
    def control_components(self):
        """
        Controls the commands given to the components
        """
        raise NotImplementedError("Method has to be implemented by subclasses")

    def control_loop(self):
        """
        Control loop for the program.
        """
        self.logger.log(f"{self.name} control loop started", LogLevel.INFO)

        while not self.paused and not self.finished:
            self.control_components()

            self.turntable.update()
            self.reflector.update()

            time.sleep(PROGRAM_UPDATE_INTERVAL_IN_SECONDS)

    def get_name(self):
        """
        Get the name of the program.
        """
        return self.name

    def start(self):
        """
        Start the program.
        """
        self.logger.log(f"{self.name} is starting", LogLevel.INFO)

        self.running = True
        self.paused = False

        self.door.lock()
        self.magnetron.start()
        self.cooling_fan.start()

        while self.running and not self.finished:
            self.control_loop()

            if not self.finished:
                with self.pause_condition:
                    self.logger.log(f"Paused {self.name}", LogLevel.INFO)
                    self.pause_condition.wait_for(lambda: not self.paused or not self.running)

        self.stop_components()

    def pause(self):
        """
        Pause the program.
        """
        self.logger.log(f"Pausing {self.name}", LogLevel.INFO)

        self.paused = True

    def resume(self):
        """
        Resume the program.
        """
        self.logger.log(f"Resuming {self.name}", LogLevel.INFO)

        self.paused = False

        with self.pause_condition:
            self.pause_condition.notify_all()

    def stop(self):
        """
        Stop the program.
        """
        self.logger.log(f"Stopping {self.name}", LogLevel.INFO)

        self.paused = True
        self.running = False

    def emergency_stop(self):
        """
        Stops all components immediately
        """
        self.logger.log(f"Emergency stopping {self.name}", LogLevel.INFO)

        self.stop()

        for component in self.components:
            component.emergency_stop()

        self.door.unlock()

    def stop_components(self):
        """
        Stops all components
        """
        self.logger.log(f"Stopping all components from {self.name}", LogLevel.INFO)

        for component in self.components:
            component.stop()

        self.door.unlock()
