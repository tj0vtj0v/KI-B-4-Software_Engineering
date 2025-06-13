from src.components.sensor.SimulationSensor import SimulationSensor
from src.components.sensor.SimulationSensorHumidity import SimulationSensorHumidity
from src.components.sensor.SimulationSensorMagnetronTemp1 import SimulationSensorMagnetronTemp1
from src.components.sensor.SimulationSensorMagnetronTemp2 import SimulationSensorMagnetronTemp2
from src.components.sensor.SimulationSensorTemp1 import SimulationSensorTemp1
from src.components.sensor.SimulationSensorTemp2 import SimulationSensorTemp2
from src.components.sensor.SimulationSensorWeight import SimulationSensorWeight
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class SensorManager:
    """
    Singleton class responsible for managing all simulation sensors in the system.
    Provides methods to update, reset, and retrieve sensor values.
    """

    _instance: 'SensorManager' = None

    def __new__(cls) -> 'SensorManager':
        """
        Ensures only one instance of SensorManager exists (Singleton pattern).

        :return: The singleton instance of SensorManager.
        :rtype: SensorManager
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes all simulation sensors and the logger.
        """
        self.logger: Logger = Logger("Sensors")

        self.temp1_sensor: SimulationSensorTemp1 = SimulationSensorTemp1()
        self.temp2_sensor: SimulationSensorTemp2 = SimulationSensorTemp2()
        self.humidity_sensor: SimulationSensorHumidity = SimulationSensorHumidity()
        self.weight_sensor: SimulationSensorWeight = SimulationSensorWeight()

        self.magnetron_temp1_sensor: SimulationSensorMagnetronTemp1 = SimulationSensorMagnetronTemp1()
        self.magnetron_temp2_sensor: SimulationSensorMagnetronTemp2 = SimulationSensorMagnetronTemp2()

        self.sensors: list[SimulationSensor] = [
            self.temp1_sensor,
            self.temp2_sensor,
            self.humidity_sensor,
            self.weight_sensor,
            self.magnetron_temp1_sensor,
            self.magnetron_temp2_sensor
        ]

    def update_sensors(self) -> None:
        """
        Updates all sensors and logs their current values.

        :return: None
        """
        self.logger.log("Updating all sensors", LogLevel.DEBUG)
        for sensor in self.sensors:
            sensor.update()

        self.logger.log(f"Magnetron Temp 1: {self.magnetron_temp1()}", LogLevel.DEBUG)
        self.logger.log(f"Magnetron Temp 2: {self.magnetron_temp2()}", LogLevel.DEBUG)
        self.logger.log(f"Inner Temp 1: {self.inner_temp1()}", LogLevel.DEBUG)
        self.logger.log(f"Inner Temp 2: {self.inner_temp2()}", LogLevel.DEBUG)
        self.logger.log(f"Inner Weight: {self.inner_weight()}", LogLevel.DEBUG)
        self.logger.log(f"Inner humidity: {self.inner_humidity()}", LogLevel.DEBUG)

    def reset(self) -> None:
        """
        Resets all sensors to their initial state.

        :return: None
        """
        self.logger.log("Resetting all sensors", LogLevel.INFO)
        for sensor in self.sensors:
            sensor.reset()

    def inner_temp1(self) -> float:
        """
        Retrieves the current value from the first inner temperature sensor.

        :return: The current temperature value from temp1_sensor.
        :rtype: float
        """
        return self.temp1_sensor.get()

    def inner_temp2(self) -> float:
        """
        Retrieves the current value from the second inner temperature sensor.

        :return: The current temperature value from temp2_sensor.
        :rtype: float
        """
        return self.temp2_sensor.get()

    def inner_humidity(self) -> float:
        """
        Retrieves the current value from the inner humidity sensor.

        :return: The current humidity value from humidity_sensor.
        :rtype: float
        """
        return self.humidity_sensor.get()

    def inner_weight(self) -> float:
        """
        Retrieves the current value from the inner weight sensor.

        :return: The current weight value from weight_sensor.
        :rtype: float
        """
        return self.weight_sensor.get()

    def magnetron_temp1(self) -> float:
        """
        Retrieves the current value from the first magnetron temperature sensor.

        :return: The current temperature value from magnetron_temp1_sensor.
        :rtype: float
        """
        return self.magnetron_temp1_sensor.get()

    def magnetron_temp2(self) -> float:
        """
        Retrieves the current value from the second magnetron temperature sensor.

        :return: The current temperature value from magnetron_temp2_sensor.
        :rtype: float
        """
        return self.magnetron_temp2_sensor.get()
