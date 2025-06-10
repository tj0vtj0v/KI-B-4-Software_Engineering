from src.helper.config import TURNTABLE_WEIGHT_IN_GRAMS, PROGRAM_DEFROSTING_TARGET_TEMP, AMBIENT_TEMPERATURE_IN_CELSIUS
from src.helper.logging.LogLevel import LogLevel
from src.program.Program import Program


class DefrostingProgram(Program):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DefrostingProgram, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

        self.name = "Defrosting Program"
        self.running = False
        self.paused = False
        self.just_updated = False

        self.cycles = max(1, (self.sensors.inner_weight() - TURNTABLE_WEIGHT_IN_GRAMS) // 100)
        self.logger.log(f"Defrosting will take {self.cycles} cycles")

    def control_components(self):
        inner_temp = (self.sensors.inner_temp1() + self.sensors.inner_temp2()) / 2

        if inner_temp > PROGRAM_DEFROSTING_TARGET_TEMP and not self.just_updated:
            self.magnetron.set_target_power_share(0.0)
            self.cycles -= 1
            self.just_updated = True

            self.logger.log(f"Defrosting cycle finished: {self.cycles} left", LogLevel.INFO)
        elif self.just_updated:
            if inner_temp < AMBIENT_TEMPERATURE_IN_CELSIUS + 5:
                self.just_updated = False
        else:
            self.magnetron.set_target_power_share(min(0.4, 0.1 + self.cycles * 0.1))

        if self.cycles <= 0:
            self.logger.log(f"Finished {self.name}", LogLevel.INFO)
            self.finished = True

    def start(self):
        self.turntable.set_speed(2)

        super().start()
