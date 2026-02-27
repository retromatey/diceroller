import argparse
import json
from importlib.metadata import PackageNotFoundError, version

from diceroller.core import CustomRandom, DiceRoller


def _project_version() -> str:
    try:
        return version("diceroller")  # must match [project].name in pyproject.toml
    except PackageNotFoundError:
        return "unknown"

def main() -> None:
    parser = argparse.ArgumentParser(description="Roll some dice 🎲")
    parser.add_argument("--version", action="version", version=_project_version())
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
    elif args.verbose:
        print(f"{data}")
    else:
        print(total)

if __name__ == "__main__":
    main()
