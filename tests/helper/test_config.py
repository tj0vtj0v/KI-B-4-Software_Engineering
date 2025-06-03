import unittest

import src.helper.config as config


class TestConfig(unittest.TestCase):
    def test_MAIN_LOOP_TIMEOUT_IN_SECONDS__exists_and_is_float(self):
        self.assertTrue(hasattr(config, "MAIN_LOOP_TIMEOUT_IN_SECONDS"))
        self.assertIsInstance(config.MAIN_LOOP_TIMEOUT_IN_SECONDS, float)

    def test_DEFAULT_LOG_LEVEL__exists_and_is_str(self):
        self.assertTrue(hasattr(config, "DEFAULT_LOG_LEVEL"))
        self.assertIsInstance(config.DEFAULT_LOG_LEVEL, str)

    def test_AMBIENT_TEMPERATURE_IN_CELSIUS__exists_and_is_float(self):
        self.assertTrue(hasattr(config, "AMBIENT_TEMPERATURE_IN_CELSIUS"))
        self.assertIsInstance(config.AMBIENT_TEMPERATURE_IN_CELSIUS, float)

    def test_AMBIENT_HUMIDITY_IN_PERCENT__exists_and_is_float(self):
        self.assertTrue(hasattr(config, "AMBIENT_HUMIDITY_IN_PERCENT"))
        self.assertIsInstance(config.AMBIENT_HUMIDITY_IN_PERCENT, float)

    def test_TURNTABLE_WEIGHT_IN_GRAMS__exists_and_is_int(self):
        self.assertTrue(hasattr(config, "TURNTABLE_WEIGHT_IN_GRAMS"))
        self.assertIsInstance(config.TURNTABLE_WEIGHT_IN_GRAMS, int)

    def test_MAGNETRON_ON_OFF_INTERVAL_IN_MS__exists_and_is_int(self):
        self.assertTrue(hasattr(config, "MAGNETRON_ON_OFF_INTERVAL_IN_MS"))
        self.assertIsInstance(config.MAGNETRON_ON_OFF_INTERVAL_IN_MS, int)

    def test_MAGNETRON_MAX_POWER_IN_WATTS__exists_and_is_int(self):
        self.assertTrue(hasattr(config, "MAGNETRON_MAX_POWER_IN_WATTS"))
        self.assertIsInstance(config.MAGNETRON_MAX_POWER_IN_WATTS, int)

    def test_MAGNETRON_MAX_POWER_SHARE_PER_MINUTE__exists_and_is_float(self):
        self.assertTrue(hasattr(config, "MAGNETRON_MAX_POWER_SHARE_PER_MINUTE"))
        self.assertIsInstance(config.MAGNETRON_MAX_POWER_SHARE_PER_MINUTE, float)

    def test_MAGNETRON_MAX_TEMP_IN_CELSIUS__exists_and_is_float(self):
        self.assertTrue(hasattr(config, "MAGNETRON_MAX_TEMP_IN_CELSIUS"))
        self.assertIsInstance(config.MAGNETRON_MAX_TEMP_IN_CELSIUS, float)
