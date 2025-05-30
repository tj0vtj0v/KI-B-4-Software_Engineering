import unittest

import src.helper.config as config


class TestConfig(unittest.TestCase):
    def test_MAIN_LOOP_TIMEOUT_IN_SECONDS__exists_and_is_float(self):
        self.assertTrue(hasattr(config, "MAIN_LOOP_TIMEOUT_IN_SECONDS"))
        self.assertIsInstance(config.MAIN_LOOP_TIMEOUT_IN_SECONDS, float)

    def test_DEFAULT_LOG_LEVEL__exists_and_is_str(self):
        self.assertTrue(hasattr(config, "DEFAULT_LOG_LEVEL"))
        self.assertIsInstance(config.DEFAULT_LOG_LEVEL, str)
