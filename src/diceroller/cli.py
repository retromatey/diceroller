import argparse
import json
from diceroller.core import DiceRoller, CustomRandom

def main():
    parser = argparse.ArgumentParser(description="Roll some dice 🎲")
    parser.add_argument("expression", help="Dice expression (e.g., 2d6+1)")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--seed", type=int, help="Optional seed for deterministic dice rolls")

    args = parser.parse_args()

    roller = DiceRoller(custom_rng=CustomRandom(seed=args.seed))
    total = roller.roll(args.expression)
    data = roller.data

    if args.json:
        print(json.dumps(data.to_dict(), indent=2))
        #print(json.dumps({
        #    "rolls": data.rolls,
        #    "modifier": data.modifier,
        #    "total": data.total,
        #    "dice_type": data.dice_type,
        #}))
    elif args.verbose:
        print(f"{data}")
    else:
        print(total)

if __name__ == "__main__":
    main()
