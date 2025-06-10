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
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("Sensors")

        self.temp1_sensor = SimulationSensorTemp1()
        self.temp2_sensor = SimulationSensorTemp2()
        self.humidity_sensor = SimulationSensorHumidity()
        self.weight_sensor = SimulationSensorWeight()

        self.magnetron_temp1_sensor = SimulationSensorMagnetronTemp1()
        self.magnetron_temp2_sensor = SimulationSensorMagnetronTemp2()

        self.sensors: list[SimulationSensor] = [self.temp1_sensor, self.temp2_sensor, self.humidity_sensor,
                                                self.weight_sensor,
                                                self.magnetron_temp1_sensor,
                                                self.magnetron_temp2_sensor]

    def update_sensors(self):
        self.logger.log("Updating all sensors", LogLevel.DEBUG)
        for sensor in self.sensors:
            sensor.update()

        self.logger.log(f"Magnetron Temp 1: {self.magnetron_temp1()}", LogLevel.DEBUG)
        self.logger.log(f"Magnetron Temp 2: {self.magnetron_temp2()}", LogLevel.DEBUG)
        self.logger.log(f"Inner Temp 1: {self.inner_temp1()}", LogLevel.DEBUG)
        self.logger.log(f"Inner Temp 2: {self.inner_temp2()}", LogLevel.DEBUG)
        self.logger.log(f"Inner Weight: {self.inner_weight()}", LogLevel.DEBUG)
        self.logger.log(f"Inner humidity: {self.inner_humidity()}", LogLevel.DEBUG)

    def reset(self):
        self.logger.log("Resetting all sensors", LogLevel.INFO)
        for sensor in self.sensors:
            sensor.reset()

    def inner_temp1(self) -> float:
        return self.temp1_sensor.get()

    def inner_temp2(self) -> float:
        return self.temp2_sensor.get()

    def inner_humidity(self) -> float:
        return self.humidity_sensor.get()

    def inner_weight(self) -> float:
        return self.weight_sensor.get()

    def magnetron_temp1(self) -> float:
        return self.magnetron_temp1_sensor.get()

    def magnetron_temp2(self) -> float:
        return self.magnetron_temp2_sensor.get()
