from typing import override
from diceroller import DiceRoller, CustomRandom
import pytest

class CustomRandomMoc(CustomRandom):
    def __init__(self):
        self.randint_return_value = 0

    def randint_returns(self, value: int):
        self.randint_return_value = value

    @override
    def randint(self, start: int, end: int) -> int:
        return self.randint_return_value


def test_parse_dice_count():
    dr = DiceRoller(CustomRandomMoc())
    test_case = "1d6+2"
    test_result = dr.parse_dice_count(test_case)
    expected = 1
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_parse_dice_type():
    dr = DiceRoller(CustomRandomMoc())
    test_case = "1d6+2"
    test_result = dr.parse_dice_type(test_case)
    expected = 6
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_parse_no_modifier():
    dr = DiceRoller(CustomRandomMoc())
    test_case = "1d6"
    test_result = dr.parse_dice_modifier(test_case)
    expected = 0
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_parse_positive_modifier():
    dr = DiceRoller(CustomRandomMoc())
    test_case = "1d6+2"
    test_result = dr.parse_dice_modifier(test_case)
    expected = 2
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_parse_negative_modifier():
    dr = DiceRoller(CustomRandomMoc())
    test_case = "1d6-2"
    test_result = dr.parse_dice_modifier(test_case)
    expected = -2
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_roll_no_modifier():
    moc = CustomRandomMoc()
    moc.randint_returns(1)
    dr = DiceRoller(moc)
    test_case = "1d6"
    test_result = dr.roll(test_case)
    expected = 1 
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_roll_positive_modifier():
    moc = CustomRandomMoc()
    moc.randint_returns(1)
    dr = DiceRoller(moc)
    test_case = "1d6+2"
    test_result = dr.roll(test_case)
    expected = 3
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_roll_negative_modifier():
    moc = CustomRandomMoc()
    moc.randint_returns(2)
    dr = DiceRoller(moc)
    test_case = "1d6-2"
    test_result = dr.roll(test_case)
    expected = 0
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_zero_modifier_str():
    dr = DiceRoller(CustomRandomMoc())
    test_case = "1d6+0"
    test_result = dr.parse_dice_modifier(test_case)
    expected = 0
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_roll_multiple_dice():
    moc = CustomRandomMoc()
    moc.randint_returns(2)
    dr = DiceRoller(moc)
    test_case = "2d6"
    test_result = dr.roll(test_case)
    expected = 4 
    msg = f"Expected: {expected}, Actual: {test_result}"
    assert test_result == expected, msg

def test_roll_multiple_dice_with_modifier():
    moc = CustomRandomMoc()
    moc.randint_returns(2)
    dr = DiceRoller(moc)
    test_case = "2d6+2"
    test_result = dr.roll(test_case)
    expected = 6 
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
def test_validate_accepts_valid_input(expression):
    dr = DiceRoller(...)
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
def test_validate_rejects_malformed_input(expression):
    dr = DiceRoller(...)
    with pytest.raises(ValueError):
        dr.validate(expression)

@pytest.mark.parametrize("expression", [
    "1d6+",
    "1d6-",
    "1d6+-2",
    "1d6--2",
    "1d6++2",
])
def test_validate_rejects_invalid_modifier(expression):
    dr = DiceRoller(...)
    with pytest.raises(ValueError):
        dr.validate(expression)
