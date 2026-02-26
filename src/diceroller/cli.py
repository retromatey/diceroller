import argparse
import json
from pathlib import Path

import tomllib

from diceroller.core import CustomRandom, DiceRoller


def _project_version() -> str:
    root = Path(__file__).resolve().parents[2]
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.exists():
        return "unknown"
    with pyproject_path.open("rb") as stream:
        metadata = tomllib.load(stream)
    return f'{metadata.get("project", {}).get("version", "unknown")}'

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
