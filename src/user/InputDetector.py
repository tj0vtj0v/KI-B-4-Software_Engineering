from pynput import keyboard
from pynput.keyboard import Key

from src.helper.Action import Action
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class InputDetector:
    """
    Detects and handles keyboard input events, delegating actions based on user interaction.
    """

    def __init__(self) -> None:
        """
        Initializes the InputDetector, setting up the logger and keyboard listener.
        """
        self.logger: Logger = Logger("UserInteraction")
        self.delegating: bool = False
        self.listener: keyboard.Listener = keyboard.Listener(on_press=self.handle_key_event)
        self.latest_key: keyboard.Key | keyboard.KeyCode | None = None

    def start(self) -> None:
        """
        Starts the input detection by activating the keyboard listener.

        :return: None
        """
        if not self.delegating:
            self.logger.log("Starting input detection", LogLevel.INFO)
            self.delegating = True
            self.listener.start()
        else:
            self.logger.log("Input detection is already running", LogLevel.WARNING)

    def stop(self) -> None:
        """
        Stops the input detection by deactivating the keyboard listener.

        :return: None
        """
        if self.delegating:
            self.logger.log("Stopping input detection", LogLevel.INFO)
            self.delegating = False
            self.listener.stop()
        else:
            self.logger.log("Input detection is not running", LogLevel.WARNING)

    def handle_key_event(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        """
        Handles a keyboard event and stores the latest key pressed.

        :param key: The key event received from the keyboard listener.
        :type key: keyboard.Key or keyboard.KeyCode
        :return: None
        """
        self.latest_key = key

    def get_latest_action(self) -> Action | None:
        """
        Maps the latest key event to a corresponding Action, if applicable.

        :return: The detected Action, or None if no valid action is found.
        :rtype: Action or None
        """
        if not self.delegating or self.latest_key is None:
            return None

        action: Action | None = None
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
