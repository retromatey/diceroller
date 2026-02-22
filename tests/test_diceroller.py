from typing import override
from diceroller import DiceRoller, CustomRandom

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
