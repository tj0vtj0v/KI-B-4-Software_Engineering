import unittest
from unittest.mock import MagicMock

from src.components.sensor.SensorManager import SensorManager
from src.helper.logging.LogLevel import LogLevel


class TestSensorManager(unittest.TestCase):
    def setUp(self):
        SensorManager._instance = None
        self.manager = SensorManager()
        self.mock_logger = MagicMock()
        self.manager.logger = self.mock_logger

    def test_singleton_instance__multiple_instances__same_object(self):
        instance1 = SensorManager()
        instance2 = SensorManager()

        self.assertIs(instance1, instance2)

    def test_update_sensors__all_sensors__update_called(self):
        for sensor in self.manager.sensors:
            sensor.update = MagicMock()

        self.manager.update_sensors()

        for sensor in self.manager.sensors:
            sensor.update.assert_called_once()

    def test_reset__all_sensors__reset_called(self):
        for sensor in self.manager.sensors:
            sensor.reset = MagicMock()

        self.manager.reset()

        for sensor in self.manager.sensors:
            sensor.reset.assert_called_once()

    def test_inner_temp1__valid_sensor__returns_value(self):
        self.manager.temp1_sensor.get = MagicMock(return_value=25.5)
        result = self.manager.inner_temp1()

        self.assertEqual(result, 25.5)

    def test_inner_temp2__valid_sensor__returns_value(self):
        self.manager.temp2_sensor.get = MagicMock(return_value=30.0)
        result = self.manager.inner_temp2()

        self.assertEqual(result, 30.0)

    def test_inner_humidity__valid_sensor__returns_value(self):
        self.manager.humidity_sensor.get = MagicMock(return_value=60.0)
        result = self.manager.inner_humidity()

        self.assertEqual(result, 60.0)

    def test_inner_weight__valid_sensor__returns_value(self):
        self.manager.weight_sensor.get = MagicMock(return_value=5.0)
        result = self.manager.inner_weight()

        self.assertEqual(result, 5.0)

    def test_magnetron_temp1__valid_sensor__returns_value(self):
        self.manager.magnetron_temp1_sensor.get = MagicMock(return_value=80.0)
        result = self.manager.magnetron_temp1()

        self.assertEqual(result, 80.0)

    def test_magnetron_temp2__valid_sensor__returns_value(self):
        self.manager.magnetron_temp2_sensor.get = MagicMock(return_value=85.0)
        result = self.manager.magnetron_temp2()

        self.assertEqual(result, 85.0)

    def test_update_sensors__logs_debug_message__expected_log(self):
        self.manager.update_sensors()

        self.mock_logger.log.assert_any_call("Updating all sensors", LogLevel.DEBUG)

    def test_reset__logs_info_message__expected_log(self):
        self.manager.reset()

        self.mock_logger.log.assert_called_with("Resetting all sensors", LogLevel.INFO)

    def test_update_sensors__logs_sensor_values__expected_logs(self):
        self.manager.magnetron_temp1_sensor.get = MagicMock(return_value=80.0)
        self.manager.magnetron_temp2_sensor.get = MagicMock(return_value=85.0)
        self.manager.temp1_sensor.get = MagicMock(return_value=25.5)
        self.manager.temp2_sensor.get = MagicMock(return_value=30.0)
        self.manager.weight_sensor.get = MagicMock(return_value=5.0)
        self.manager.humidity_sensor.get = MagicMock(return_value=60.0)

        self.manager.update_sensors()

        self.mock_logger.log.assert_any_call("Magnetron Temp 1: 80.0", LogLevel.DEBUG)
        self.mock_logger.log.assert_any_call("Magnetron Temp 2: 85.0", LogLevel.DEBUG)
        self.mock_logger.log.assert_any_call("Inner Temp 1: 25.5", LogLevel.DEBUG)
        self.mock_logger.log.assert_any_call("Inner Temp 2: 30.0", LogLevel.DEBUG)
        self.mock_logger.log.assert_any_call("Inner Weight: 5.0", LogLevel.DEBUG)
        self.mock_logger.log.assert_any_call("Inner humidity: 60.0", LogLevel.DEBUG)

    def test_inner_temp1__sensor_raises_exception__raises_exception(self):
        self.manager.temp1_sensor.get = MagicMock(side_effect=Exception("Sensor error"))

        with self.assertRaises(Exception) as context:
            self.manager.inner_temp1()

        self.assertEqual(str(context.exception), "Sensor error")
