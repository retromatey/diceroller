from diceroller import DiceRoller

def demo(roll: str):
    dr = DiceRoller()
    result = dr.roll(roll)
    print(f"The roll was {roll} and the result is {result}")
    print(dr.diceRollerData)

rolls = ["1d6", "1d6+2", "1d6-2", "1d20", "1d20+2", "1d20-2"]

for roll in rolls:
    demo(roll)
