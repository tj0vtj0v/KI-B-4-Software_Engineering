import unittest
from unittest.mock import MagicMock, patch

from src.components.door.Door import Door
from src.components.light.Light import Light
from src.components.light.LightController import LightController
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel
from src.program.ProgramController import ProgramController


class TestLightController(unittest.TestCase):

    def setUp(self):
        self.light_controller = None
        self.light_controller = LightController()
        self.light_controller.logger = MagicMock(spec=Logger)
        self.light_controller.light = MagicMock(spec=Light)
        self.light_controller.door = MagicMock(spec=Door)
        self.light_controller.program = MagicMock(spec=ProgramController)

    def test___new___instance_created__singleton(self):
        instance1 = LightController()
        instance2 = LightController()

        self.assertIs(instance1, instance2)

    def test_start__not_running__starts_thread(self):
        self.light_controller.running = False

        with patch("threading.Thread") as mock_thread:
            self.light_controller.start()

            self.assertTrue(self.light_controller.running)
            mock_thread.assert_called_once_with(target=self.light_controller.light_loop, name="LightThread")
            mock_thread.return_value.start.assert_called_once()

    def test_start__already_running__logs_warning(self):
        self.light_controller.running = True
        self.light_controller.start()

        self.light_controller.logger.log.assert_called_once_with("Light control is already running", LogLevel.WARNING)

    def test_stop__running__stops_thread(self):
        self.light_controller.running = True
        mock_thread = MagicMock()
        self.light_controller.thread = mock_thread
        self.light_controller.stop()

        self.assertFalse(self.light_controller.running)

        mock_thread.join.assert_called_once()
        self.light_controller.logger.log.assert_called_once_with("Stopping light control", LogLevel.INFO)

    def test_stop__not_running__logs_warning(self):
        self.light_controller.running = False
        self.light_controller.stop()

        self.light_controller.logger.log.assert_called_once_with("Light control is not running", LogLevel.WARNING)

    def test_light_cycle__door_opened__turns_light_on(self):
        self.light_controller.door.opened = True
        self.light_controller.light.on = False
        self.light_controller.light_cycle()

        self.assertTrue(self.light_controller.light.on)
        self.light_controller.logger.log.assert_called_once_with("Light turned on", LogLevel.INFO)

    def test_light_cycle__program_running__turns_light_on(self):
        self.light_controller.door.opened = False
        self.light_controller.light.on = False
        self.light_controller.program.is_running.return_value = True
        self.light_controller.program.is_paused.return_value = False
        self.light_controller.program.is_finished.return_value = False
        self.light_controller.light_cycle()

        self.assertTrue(self.light_controller.light.on)
        self.light_controller.logger.log.assert_called_once_with("Light turned on", LogLevel.INFO)

    def test_light_cycle__door_closed_and_program_stopped__turns_light_off(self):
        self.light_controller.door.opened = False
        self.light_controller.light.on = True
        self.light_controller.program.is_running.return_value = False
        self.light_controller.light_cycle()

        self.assertFalse(self.light_controller.light.on)
        self.light_controller.logger.log.assert_called_once_with("Light turned off", LogLevel.INFO)

    def test_light_loop__running__calls_light_cycle(self):
        self.light_controller.running = True

        with patch("time.sleep", return_value=None):
            with patch.object(self.light_controller, "light_cycle") as mock_light_cycle:
                def stop_running():
                    self.light_controller.running = False

                mock_light_cycle.side_effect = stop_running
                self.light_controller.light_loop()

                mock_light_cycle.assert_called_once()
