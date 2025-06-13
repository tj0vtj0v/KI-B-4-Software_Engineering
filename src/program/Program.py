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
    Abstract base class for a program that controls various hardware components.

    This class provides the structure for starting, pausing, resuming, stopping,
    and emergency stopping of a program, as well as managing the control loop
    and component interactions.
    """

    pause_condition: threading.Condition = threading.Condition()
    logger: Logger = Logger("ProgramControl")
    sensors: SensorManager = SensorManager()
    door: DoorController = DoorController()
    magnetron: MagnetronModulator = MagnetronModulator()
    cooling_fan: CoolingFanController = CoolingFanController()
    turntable: TurntableController = TurntableController()
    reflector: ReflectorController = ReflectorController()
    components: list = [magnetron, cooling_fan, turntable, reflector]

    def __init__(self) -> None:
        """
        Initializes the Program instance with default state variables.
        """
        self.name: str = "Program"
        self.paused: bool = False
        self.running: bool = False
        self.finished: bool = False

    @abstractmethod
    def control_components(self) -> None:
        """
        Abstract method to control the commands given to the components.

        :raises NotImplementedError: If not implemented by subclasses.
        """
        raise NotImplementedError("Method has to be implemented by subclasses")

    def control_loop(self) -> None:
        """
        Control loop for the program.

        This loop repeatedly calls `control_components` and updates the turntable
        and reflector components at a fixed interval, until the program is paused or finished.
        """
        self.logger.log(f"{self.name} control loop started", LogLevel.INFO)

        while not self.paused and not self.finished:
            self.control_components()
            self.turntable.update()
            self.reflector.update()
            time.sleep(PROGRAM_UPDATE_INTERVAL_IN_SECONDS)

    def get_name(self) -> str:
        """
        Get the name of the program.

        :return: The name of the program.
        :rtype: str
        """
        return self.name

    def start(self) -> None:
        """
        Start the program.

        This method sets the running state, locks the door, starts the magnetron and cooling fan,
        and enters the main control loop. If paused, it waits until resumed.
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

        self.paused = False
        self.running = False

        self.stop_components()

    def pause(self) -> None:
        """
        Pause the program.

        Sets the paused state to True and logs the action.
        """
        self.logger.log(f"Pausing {self.name}", LogLevel.INFO)
        self.paused = True

    def resume(self) -> None:
        """
        Resume the program.

        Sets the paused state to False, notifies all waiting threads, and logs the action.
        """
        self.logger.log(f"Resuming {self.name}", LogLevel.INFO)
        self.paused = False

        with self.pause_condition:
            self.pause_condition.notify_all()

    def stop(self) -> None:
        """
        Stop the program.

        Sets the paused and running states to False and logs the action.
        """
        self.logger.log(f"Stopping {self.name}", LogLevel.INFO)
        self.paused = True
        self.running = False

    def emergency_stop(self) -> None:
        """
        Stops all components immediately.

        Calls `stop` and then performs an emergency stop on all components and unlocks the door.
        """
        self.logger.log(f"Emergency stopping {self.name}", LogLevel.INFO)
        self.stop()

        for component in self.components:
            component.emergency_stop()

        self.door.unlock()

    def stop_components(self) -> None:
        """
        Stops all components.

        Iterates through all components and calls their `stop` method, then unlocks the door.
        """
        self.logger.log(f"Stopping all components from {self.name}", LogLevel.INFO)

        for component in self.components:
            component.stop()

        self.door.unlock()
