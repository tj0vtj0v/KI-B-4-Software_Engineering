from src.helper.exceptions import MockException


class MockProgramController:
    def __init__(self):
        self.active = False

    def start(self):
        self.active = True

    def update(self):
        assert self.active

    def mock_error(self):
        raise MockException()

    def stop(self):
        self.active = False
