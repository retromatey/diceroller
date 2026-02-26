import pytest
from typing_extensions import override

from diceroller.core import CustomRandom, DiceRoller


class CustomRandomMoc(CustomRandom):
    def __init__(self) -> None:
        self.randint_return_value = 0

    def randint_returns(self, value: int) -> None:
        self.randint_return_value = value

    @override
    def randint(self, start: int, end: int) -> int:
        return self.randint_return_value

@pytest.mark.parametrize(
    "expression, mock_value, expected",
    [
        ("1d6", 3, 3),
        ("2d6", 3, 6),
        ("2d6-3", 3, 3),
        ("2d6+3", 3, 9),
    ],
)
def test_roll_valid_cases(expression: str, mock_value: int, expected: int) -> None:
    moc = CustomRandomMoc()
    moc.randint_returns(mock_value)
    dr = DiceRoller(moc)
    test_result = dr.roll(expression)
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

@pytest.mark.parametrize("expression", [
    "1d6",
    "2d8",
    "2d6+0",
    "2D8",
    "2D8+2",
    "10d20",
    "1d6+2",
    "3d4-1",
    "01d06",
    " 3d4-1 ",
])
def test_validate_accepts_valid_input(expression: str) -> None:
    dr = DiceRoller()
    dr.validate(expression)  # should not raise

@pytest.mark.parametrize("expression", [
    "d6",
    "2d",
    "2x6",
    "2dd6",
    "",
    "abc",
    "2d6d4",
    "1d6 + 2",  # (whitespace not allowed inside expression)
    " 1 d6",    # (whitespace not allowed inside expression)
    "1 d6",     # (whitespace not allowed inside expression)
    "1d 6",     # (whitespace not allowed inside expression)
    "1d6+ 2",   # (whitespace not allowed inside expression)
    "1d6 -2",   # (whitespace not allowed inside expression)
    "1d6 - 2",  # (whitespace not allowed inside expression)
    "0d6",      # (count must be >= 1)
    "-1d6",     # (count must be >= 1)
    "1d0",      # (type must be >= 1)
    "1d-6",     # (type must be >= 1)
])
def test_validate_rejects_malformed_input(expression: str) -> None:
    dr = DiceRoller()
    with pytest.raises(ValueError):
        dr.validate(expression)

@pytest.mark.parametrize("expression", [
    "1d6+",
    "1d6-",
    "1d6+-2",
    "1d6--2",
    "1d6++2",
])
def test_validate_rejects_invalid_modifier(expression: str) -> None:
    dr = DiceRoller()
    with pytest.raises(ValueError):
        dr.validate(expression)
