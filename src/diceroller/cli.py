import argparse
import json
from diceroller.core import DiceRoller

def main():
    parser = argparse.ArgumentParser(description="Roll some dice 🎲")
    parser.add_argument("expression", help="Dice expression (e.g., 2d6+1)")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    roller = DiceRoller()
    total = roller.roll(args.expression)
    data = roller.data

    if args.json:
        print(json.dumps({
            "rolls": data.rolls,
            "modifier": data.modifier,
            "total": data.total,
        }))
    elif args.verbose:
        print(f"{data}")
    else:
        print(total)

if __name__ == "__main__":
    main()
