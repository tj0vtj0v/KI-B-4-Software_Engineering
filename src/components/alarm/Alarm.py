class Alarm:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Alarm, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.active = False
