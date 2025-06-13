import unittest
from unittest.mock import patch, MagicMock

from src.main import main


class TestMain(unittest.TestCase):
    def setUp(self):
        patch('src.user.InputDetector.InputDetector.__init__', return_value=None)

    @patch("src.main.time.sleep", return_value=None)
    @patch("src.main.SystemControl")
    def test_main__system_control_start_called__success(self, mock_system_control, mock_sleep):
        mock_system_instance = MagicMock()
        mock_system_control.return_value = mock_system_instance

        main()

        mock_system_control.assert_called_once()
        mock_system_instance.start.assert_called_once()

    @patch("src.main.time.sleep", return_value=None)
    @patch("src.main.SystemControl")
    def test_main__time_sleep_called_with_1__success(self, mock_system_control, mock_sleep):
        main()

        mock_sleep.assert_any_call(1)
