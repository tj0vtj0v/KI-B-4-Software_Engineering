class Magnetron:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Magnetron, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.active = False

    def turn_on(self):
        self.active = True

    def turn_off(self):
        self.active = False
