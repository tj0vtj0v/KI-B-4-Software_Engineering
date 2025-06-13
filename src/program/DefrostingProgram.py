from src.helper.config import TURNTABLE_WEIGHT_IN_GRAMS, PROGRAM_DEFROSTING_TARGET_TEMP, AMBIENT_TEMPERATURE_IN_CELSIUS
from src.helper.logging.LogLevel import LogLevel
from src.program.Program import Program


class DefrostingProgram(Program):
    """
    Program for defrosting using a microwave oven.

    Calculates the number of defrosting cycles based on the weight detected by sensors.
    Controls the magnetron and turntable to achieve the target defrosting temperature.

    :ivar name: Name of the program.
    :ivar running: Indicates if the program is running.
    :ivar paused: Indicates if the program is paused.
    :ivar just_updated: Indicates if the state was just updated after a cycle.
    :ivar cycles: Number of remaining defrosting cycles.
    """

    def __init__(self) -> None:
        """
        Initialize the DefrostingProgram.

        Sets up the program name, state flags, and calculates the number of cycles based on the inner weight.

        :return: None
        """
        super().__init__()

        self.name: str = "Defrosting Program"
        self.running: bool = False
        self.paused: bool = False
        self.just_updated: bool = False

        self.cycles: int = max(1, (self.sensors.inner_weight() - TURNTABLE_WEIGHT_IN_GRAMS) // 100)
        self.logger.log(f"Defrosting will take {self.cycles} cycles")

    def control_components(self) -> None:
        """
        Control the components (magnetron, turntable) during the defrosting process.

        Adjusts the magnetron power and manages the cycle state based on temperature readings.

        :return: None
        """
        inner_temp: float = (self.sensors.inner_temp1() + self.sensors.inner_temp2()) / 2

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

    def start(self) -> None:
        """
        Start the defrosting program.

        Sets the turntable speed and calls the parent start method.

        :return: None
        """
        self.turntable.set_speed(2)

        super().start()
