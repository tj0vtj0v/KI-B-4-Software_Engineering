import threading
import time

from src.components.cooling.CoolingFan import CoolingFan
from src.components.sensor.SensorManager import SensorManager
from src.helper.Logger import Logger
from src.helper.config import COOLING_FAN_STEP_IN_PERCENT, COOLING_FAN_UPDATE_INTERVAL_IN_SECONDS
from src.helper.logging.LogLevel import LogLevel


class CoolingFanController:
    """
    Singleton controller for managing the cooling fan based on sensor data.

    This class handles the logic for starting, stopping, and adjusting the cooling fan's power share
    according to the temperature readings from the magnetron sensors.
    """

    _instance: "CoolingFanController" = None

    def __new__(cls) -> "CoolingFanController":
        """
        Ensures only one instance of CoolingFanController exists.

        :return: The singleton instance of CoolingFanController.
        :rtype: CoolingFanController
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the CoolingFanController with required components and state variables.
        """
        self.logger: Logger = Logger("CoolingControl")
        self.cooling_fan: CoolingFan = CoolingFan()
        self.sensors: SensorManager = SensorManager()
        self.target_power_share: float = 0.0

        self.cooldown: bool = False
        self.emergency: bool = False
        self.running: bool = False
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        """
        Starts the cooling fan control loop in a separate thread.

        :return: None
        """
        if not self.running:
            self.logger.log("Starting Cooling Fan", LogLevel.INFO)

            self.running = True
            self.thread = threading.Thread(target=self.cooling_fan_loop, name="CoolingThread")
            self.thread.start()
        else:
            self.logger.log("Cooling Fan is already running", LogLevel.WARNING)

    def stop(self) -> None:
        """
        Initiates a cooldown stop for the cooling fan.

        :return: None
        """
        if self.running:
            self.logger.log("Stopping Cooling Fan", LogLevel.INFO)

            self.cooldown = True
        else:
            self.logger.log("Cooling Fan is already stopped", LogLevel.WARNING)

    def emergency_stop(self) -> None:
        """
        Immediately stops the cooling fan and waits for the control thread to finish.

        :return: None
        """
        if self.running:
            self.logger.log("Emergency stopping Cooling Fan", LogLevel.INFO)

            self.emergency = True
            if self.thread:
                self.thread.join()
        else:
            self.logger.log("Cooling Fan is already stopped", LogLevel.WARNING)

    @staticmethod
    def magnetron_temp_to_power_share(magnetron_temp: float) -> float:
        """
        Converts the magnetron temperature to a power share value for the cooling fan.

        :param magnetron_temp: The average temperature of the magnetron in degrees Celsius.
        :type magnetron_temp: float
        :return: The calculated power share (0.0 to 1.0).
        :rtype: float
        """
        if magnetron_temp <= 50.0:
            return 0.0
        elif magnetron_temp <= 100.0:
            return (magnetron_temp - 50.0) / 200.0
        elif magnetron_temp < 150.0:
            return 0.25 + (magnetron_temp - 100.0) * 0.015
        else:
            return 1.0

    def cooling_fan_cycle(self) -> None:
        """
        Executes a single control cycle for the cooling fan, updating its power share based on sensor data.

        :return: None
        """
        self.logger.log(f"Updating Cooling Fan - currently at {self.target_power_share}%", LogLevel.DEBUG)
        magnetron_temp: float = (self.sensors.magnetron_temp1() + self.sensors.magnetron_temp2()) / 2.0

        self.target_power_share = self.magnetron_temp_to_power_share(magnetron_temp)

        if (self.cooldown and self.target_power_share <= COOLING_FAN_STEP_IN_PERCENT) or self.emergency:
            self.running = False
            self.logger.log("Cooling Fan is stopped", LogLevel.INFO)

            return

        if self.cooling_fan.power_share != self.target_power_share:
            if abs(self.target_power_share - self.cooling_fan.power_share) <= COOLING_FAN_STEP_IN_PERCENT:
                self.cooling_fan.power_share = self.target_power_share
            else:
                if self.target_power_share > self.cooling_fan.power_share:
                    self.cooling_fan.power_share += COOLING_FAN_STEP_IN_PERCENT
                else:
                    self.cooling_fan.power_share -= COOLING_FAN_STEP_IN_PERCENT

        self.cooling_fan.power_share = max(0.0, min(self.cooling_fan.power_share, 1.0))

    def cooling_fan_loop(self) -> None:
        """
        Main loop for controlling the cooling fan, running in a separate thread.

        :return: None
        """
        self.logger.log("Cooling Fan loop starting", LogLevel.INFO)

        while self.running:
            self.cooling_fan_cycle()
            time.sleep(COOLING_FAN_UPDATE_INTERVAL_IN_SECONDS)
