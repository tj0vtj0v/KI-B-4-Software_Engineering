from pynput import keyboard
from pynput.keyboard import Key

from src.helper.Action import Action
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class InputDetector:
    def __init__(self):
        self.logger = Logger("UserInteraction")
        self.delegating = False
        self.listener = keyboard.Listener(on_press=self.handle_key_event)

        self.latest_key = None

    def start(self):
        if not self.delegating:
            self.logger.log("Starting input detection", LogLevel.INFO)
            self.delegating = True
            self.listener.start()
        else:
            self.logger.log("Input detection is already running", LogLevel.WARNING)

    def stop(self):
        if self.delegating:
            self.logger.log("Stopping input detection", LogLevel.INFO)
            self.delegating = False
            self.listener.stop()
        else:
            self.logger.log("Input detection is not running", LogLevel.WARNING)

    def handle_key_event(self, key):
        self.latest_key = key

    def get_latest_action(self):
        if not self.delegating or self.latest_key is None:
            return None

        action = None
        match self.latest_key.char if hasattr(self.latest_key, "char") else self.latest_key:
            case Key.esc:
                action = Action.OFF
            case Key.enter:
                action = Action.START
            case 'o':
                action = Action.OPEN_DOOR
            case 'c':
                action = Action.CLOSE_DOOR
            case 's':
                action = Action.STOP
            case 'p':
                action = Action.PAUSE
            case 'r':
                action = Action.RESUME

        self.latest_key = None

        if action is not None:
            return action

        return None
