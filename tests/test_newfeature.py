# Pytest is not used here
import pytest


@pytest.mark.skip(reason="This is supposed to be impossible")
def test_impossibleTest():
    assert 4 == 5


def test_possibleTest():
    assert 4 == 4
