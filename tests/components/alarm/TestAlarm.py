from src.components.alarm.Alarm import Alarm


def test_init__initial_state__active_is_false():
    alarm = Alarm()
    assert alarm.active is False
