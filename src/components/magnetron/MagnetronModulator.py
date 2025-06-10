import random
import threading
import time

from src.components.magnetron.Magnetron import Magnetron
from src.components.magnetron.MagnetronRingbuffer import MagnetronRingbuffer
from src.components.sensor.SensorManager import SensorManager
from src.helper.Logger import Logger
from src.helper.config import MAGNETRON_ON_OFF_INTERVAL_IN_SECONDS, MAGNETRON_MAX_POWER_SHARE_PER_MINUTE, \
    MAGNETRON_MAX_TEMP_IN_CELSIUS
from src.helper.logging.LogLevel import LogLevel


class MagnetronModulator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MagnetronModulator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("MagnetronControl")
        self.power_history = MagnetronRingbuffer(60 // MAGNETRON_ON_OFF_INTERVAL_IN_SECONDS)

        self.sensor_manager = SensorManager()
        self.magnetron = Magnetron()
        self.target_power_share = 0

        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.logger.log("Starting Magnetron control", LogLevel.INFO)

            self.running = True
            self.thread = threading.Thread(target=self.magnetron_loop)
            self.thread.start()
        else:
            self.logger.log("Magnetron control is already running", LogLevel.WARNING)

    def stop(self):
        if self.running:
            self.logger.log("Stopping Magnetron control", LogLevel.INFO)

            self.running = False
            if self.thread:
                self.thread.join()

            self.magnetron.turn_off()
        else:
            self.logger.log("Magnetron control is already stopped", LogLevel.WARNING)

    def emergency_stop(self):
        self.logger.log("Emergency stopping Magnetron control", LogLevel.INFO)
        self.stop()

    def set_target_power_share(self, power_share_in_percent: float):
        if power_share_in_percent < 0 or power_share_in_percent > 1:
            raise ValueError("Power share must be between 0 and 1")

        if power_share_in_percent == self.target_power_share:
            return

        self.target_power_share = power_share_in_percent
        self.logger.log(f"Target power set to {power_share_in_percent}%", LogLevel.INFO)

    def safety_hazard(self):
        if self.power_history.power_share() > MAGNETRON_MAX_POWER_SHARE_PER_MINUTE:
            self.logger.log("Power share limit exceeded, skipping magnetron cycle", LogLevel.WARNING)
            return True

        magnetron_max_temp = max(self.sensor_manager.magnetron_temp1(), self.sensor_manager.magnetron_temp2())

        if magnetron_max_temp > MAGNETRON_MAX_TEMP_IN_CELSIUS:
            self.logger.log(f"Magnetron temperature {magnetron_max_temp} exceeds limit, skipping cycle",
                            LogLevel.WARNING)
            return True

        return False

    def magnetron_cycle(self):
        self.logger.log(f"Updating Magnetron - currently at {self.target_power_share}%", LogLevel.DEBUG)

        if self.safety_hazard() or random.uniform(0, 1) >= self.target_power_share:
            self.power_history.add(False)
            self.magnetron.turn_off()
        else:
            self.power_history.add(True)
            self.magnetron.turn_on()

    def magnetron_loop(self):
        self.logger.log("Magnetron loop starting", LogLevel.INFO)

        while self.running:
            self.magnetron_cycle()
            time.sleep(MAGNETRON_ON_OFF_INTERVAL_IN_SECONDS)
