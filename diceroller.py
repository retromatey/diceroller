import random

class CustomRandom():
    def __init__(self):
        random.seed()

    def randint(self, start: int, end: int) -> int:
        return random.randint(start, end)

class DiceRollerData():
    def __init__(self):
        self.rolls = []
        self.modifier = 0
        self.total = 0

    def clear(self):
        self.rolls = []
        self.modifier = 0
        self.total = 0

    def set(self, rolls: list[int], modifier: int, total: int):
        self.rolls = [x for x in rolls]
        self.modifier = modifier
        self.total = total

    def __str__(self) -> str:
        result = ""
        modifier_str = ""
        if self.modifier > 0:
            modifier_str = f" +{self.modifier} "
        elif self.modifier < 0:
            modifier_str = f" {self.modifier} "
        for roll in self.rolls:
            result += f"{roll} "
        result = f"{self.total} ( {result}{modifier_str})"
        return result

class DiceRoller():
    def __init__(self, customRandom = CustomRandom()):
        self.rand = customRandom
        self.diceRollerData = DiceRollerData()

    def validate(self, expression: str) -> None:
        """Raise ValueError if the dice expression is invalid."""
        # Supported format for expression:
        # <dice_count>[d|D]<dice_type>[+|-<modifier>]
        # Where:
        #   - dice_count is a positive integer (>= 1)
        #   - dice_type is a positive integer (>= 1)
        #   - modifier is an integer (optional, can be negative)
        #   - "d" can be both lowercase or uppercase
        #
        # Valid Input Examples:
        # "1d6"
        # "2d8"
        # "10d20"
        # "1d6+2"
        # "3d4-1"
        # "100d100+999"
        # " 1d6+2 " (whitespace allowed outside of expression)
        #
        # Invalid Input Examples:
        # "d6"
        # "2d"
        # "2x6"
        # "2dd6"
        # "2d6d4"
        # "abc"
        # ""
        # "0d6" (count must be >= 1)
        # "-1d6" (count must be >= 1)
        # "1d0" (type must be >= 1)
        # "1d-6" (type must be >= 1)
        # "1d6+" (modifier violation)
        # "1d6+-2" (modifier violation)
        # "1d6--2" (modifier violation)
        # "1d6 + 2" (whitespace not allowed inside expression)
        pass

    def roll(self, roll: str) -> int:
        self.validate(roll)
        self.diceRollerData.clear()
        dice_count = self.parse_dice_count(roll)
        dice_type = self.parse_dice_type(roll)
        dice_modifier = self.parse_dice_modifier(roll)
        rolls = []
        for roll in range(0, dice_count):
            rolls.append(self.rand.randint(1, dice_type))
        roll_total = sum(rolls)
        total = roll_total + dice_modifier
        self.diceRollerData.set(rolls, dice_modifier, total)
        return total

    def parse_dice_count(self, roll: str) -> int:
        tokens = roll.split("d")
        count_str = tokens[0]
        count = int(count_str)
        return count

    def parse_dice_type(self, roll: str) -> int:
        tokens = roll.split("d")
        token = tokens[1]
        dice_type_str = ""
        for char in token:
            if char.isdigit():
                dice_type_str += char
            else:
                break
        dice_type = int(dice_type_str)
        return dice_type

    def parse_dice_modifier(self, roll: str) -> int:
        result = 0
        tokens = roll.split("d")
        token = tokens[1]
        if "+" in token:
            modifier_str = token.split("+")[1]
            result = int(modifier_str)
        elif "-" in token:
            modifier_str = token.split("-")[1]
            result = int(modifier_str) * -1
        return result

