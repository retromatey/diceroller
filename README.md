# Dice Roller

This repository implements a simple dice-rolling engine that parses expressions
like `2d6+1` and produces consistent totals. `DiceRoller` validates expressions,
rolls the requested dice using an injectable random provider, and stores the
details in `DiceRollerData` so callers can inspect each die result, the
modifier, and the final total.

## Usage

1. Import `DiceRoller` (and `CustomRandom` if you need deterministic behavior in
   tests).
2. Call `validate(expression)` to ensure user input follows the supported
   format: `<dice_count>[d|D]<dice_type>[+|-<modifier>]` with no internal
   whitespace and positive integers for the count and type.
3. Call `roll(expression)` to execute the dice rolls; the injector lets unit
   tests control randomness.
4. Inspect `diceRollerData.rolls`, `.modifier`, and `.total` after rolling if
   you need the breakdown.

## Testing

Run the current test suite with:

```
PYTHONPATH=$(pwd) pytest -q
```

`PYTHONPATH` must include the project root so `tests` can import `diceroller`.

## Extending

- Add new expression formats by updating `DiceRoller.validate` and reusing the
  existing parsing helpers.
- Replace `CustomRandom` in production code if you need a different randomness
  source.
- Add tests whenever you change parsing/validation so regressions are caught
  quickly.

## Example expressions

| Expression | Meaning                                | Sample result             |
|------------|----------------------------------------|---------------------------|
| `1d6`      | Roll one six-sided die                 | 4 → total `4`             |
| `2d8+3`    | Roll two eight-sided dice, add 3       | 5 + 7 + 3 → total `15`    |
| `3D4-1`    | Roll three four-sided dice, subtract 1 | 2 + 1 + 3 - 1 → total `5` |

Run any expression through `roll()` after `validate()` to see its breakdown in
`DiceRollerData`.

## Getting started

```python3
from diceroller import DiceRoller

roller = DiceRoller()
expression = "2d6+1"
roller.validate(expression)
total = roller.roll(expression)

print(f"rolls: {roller.data.rolls}")
print(f"modifier: {roller.data.modifier}")
print(f"total: {total}")
```

The above snippet validates an expression, executes it, and prints each die, the
modifier, and the total.
- Add new expression formats by updating `DiceRoller.validate` and reusing the
  existing parsing helpers.
- Replace `CustomRandom` in production code if you need a different randomness
  source.
- Add tests whenever you change parsing/validation so regressions are caught
  quickly.
