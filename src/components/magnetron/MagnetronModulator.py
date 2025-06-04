import random
import threading
import time

from src.components.magnetron.Magnetron import Magnetron
from src.components.magnetron.MagnetronRingbuffer import MagnetronRingbuffer
from src.components.sensor.SensorManager import SensorManager
from src.helper.Logger import Logger
from src.helper.config import MAGNETRON_ON_OFF_INTERVAL_IN_MS, MAGNETRON_MAX_POWER_SHARE_PER_MINUTE, \
    MAGNETRON_MAX_TEMP_IN_CELSIUS
from src.helper.logging.LogLevel import LogLevel


class MagnetronModulator:
    def __init__(self):
        self.logger = Logger("MagnetronControl")
        self.power_history = MagnetronRingbuffer((60 * 1000) // MAGNETRON_ON_OFF_INTERVAL_IN_MS)

        self.sensor_manager = SensorManager()
        self.magnetron = Magnetron()
        self.target_power_share = 0

        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.magnetron_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def set_target_power(self, power_share_in_percent: float):
        if power_share_in_percent < 0 or power_share_in_percent > 1:
            raise ValueError("Power share must be between 0 and 1")

        self.target_power_share = power_share_in_percent
        self.logger.log(f"Target power set to {power_share_in_percent} watts", level=LogLevel.INFO)

    def safety_hazard(self):
        if self.power_history.power_share() > MAGNETRON_MAX_POWER_SHARE_PER_MINUTE:
            self.logger.log("Power share limit exceeded, skipping magnetron cycle", level=LogLevel.WARNING)
            return True

        magnetron_max_temp = max(self.sensor_manager.magnetron_temp1_sensor(),
                                 self.sensor_manager.magnetron_temp2_sensor())
        if magnetron_max_temp > MAGNETRON_MAX_TEMP_IN_CELSIUS:
            self.logger.log(f"Magnetron temperature {magnetron_max_temp} exceeds limit, skipping cycle",
                            level=LogLevel.WARNING)
            return True

        return False

    def magnetron_cycle(self):
        if self.safety_hazard() or random.uniform(0, 1) >= self.target_power_share:
            self.power_history.add(False)
            self.magnetron.turn_off()
        else:
            self.power_history.add(True)
            self.magnetron.turn_on()

    def magnetron_loop(self):
        while self.running:
            self.magnetron_cycle()
            time.sleep(MAGNETRON_ON_OFF_INTERVAL_IN_MS)
