import time

from src.SystemControl import SystemControl


def main():
    system_control = SystemControl()
    system_control.start()
    time.sleep(1)


if __name__ == "__main__":
    main()
