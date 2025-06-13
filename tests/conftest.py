import sys
from unittest.mock import MagicMock

sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
