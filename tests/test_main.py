import pytest

from src.main import main


def test_main_returns_one():
    assert main() == 1
