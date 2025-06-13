import time

from src.SystemControl import SystemControl


def main() -> None:
    """
    Entry point for the application. Initializes and starts the system control.

    :return: None
    """
    system_control: SystemControl = SystemControl()
    system_control.start()
    time.sleep(1)


if __name__ == "__main__":
    main()
