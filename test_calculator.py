import pytest

from calculator import add, divide


def test_add():
    result = add(2, 3)

    assert result == 5


def test_divide():
    result = divide(10, 2)

    assert result == 5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        divide(10, 0)
