import random
import re
from typing import Any


class CustomRandom:
    def __init__(self, seed: int | None = None):
        self._rnd = random.Random() if seed is None else random.Random(seed)

    def randint(self, start: int, end: int) -> int:
        return self._rnd.randint(start, end)

class DiceRollerData:
    def __init__(self) -> None:
        self.dice_type = 0
        self.rolls: list[int] = []
        self.modifier = 0
        self.total = 0

    def clear(self) -> None:
        self.dice_type = 0
        self.rolls = []
        self.modifier = 0
        self.total = 0

    def set(self, rolls: list[int], modifier: int, total: int, dice_type: int) -> None:
        self.dice_type = dice_type
        self.rolls = [x for x in rolls]
        self.modifier = modifier
        self.total = total

    def __str__(self) -> str:
        result = ""
        modifier_str = ""
        if self.modifier > 0:
            modifier_str = f"+{self.modifier} "
        elif self.modifier < 0:
            modifier_str = f"{self.modifier} "
        for roll in self.rolls:
            result += f"{roll} "
        result = f"{self.total} ( {result}{modifier_str})"
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "rolls": self.rolls,
            "modifier": self.modifier,
            "total": self.total,
            "dice_type": self.dice_type,
        }

class DiceRoller:
    def __init__(self, custom_rng: CustomRandom | None = None):
        self.rng = CustomRandom() if custom_rng is None else custom_rng
        self.diceRollerData = DiceRollerData()

    @property
    def data(self) -> DiceRollerData:
        return self.diceRollerData

    def validate(self, expression: str) -> tuple[int, int, int]:
        """Raise ValueError if the dice expression is invalid."""
        # Supported format for expression:
        # <dice_count>[d|D]<dice_type>[+|-<modifier>]
        # Where:
        #   - dice_count is a positive integer (>= 1)
        #   - dice_type is a positive integer (>= 1)
        #   - modifier is an integer (optional, can be negative)
        trimmed = expression.strip()
        if not trimmed:
            raise ValueError("dice expression cannot be empty")

        if any(char.isspace() for char in trimmed):
            raise ValueError("dice expression must not contain whitespace")

        pattern = re.compile(r"^(\d+)[dD](\d+)([+-]\d+)?$")
        match = pattern.fullmatch(trimmed)
        if not match:
            raise ValueError("dice expression not well formed")

        dice_count = int(match.group(1))
        dice_type = int(match.group(2))
        modifier = int(match.group(3) or 0)
        if dice_count < 1:
            raise ValueError("dice count must be >= 1")
        if dice_type < 1:
            raise ValueError("dice type must be >= 1")
        return (dice_count, dice_type, modifier)

    def roll(self, roll: str) -> int:
        dice_count, dice_type, dice_modifier = self.validate(roll)
        self.diceRollerData.clear()
        rolls = []
        for _ in range(0, dice_count):
            rolls.append(self.rng.randint(1, dice_type))
        roll_total = sum(rolls)
        total = roll_total + dice_modifier
        self.diceRollerData.set(rolls, dice_modifier, total, dice_type)
        return total
