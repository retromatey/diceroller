# DiceRoller

A lightweight, test-driven dice rolling engine and CLI tool.

`diceroller` parses expressions like `2d6+1`, validates them against a strict
grammar, rolls the dice, and returns structured results. It supports verbose and
JSON output modes, making it useful both for tabletop sessions and scripting.

---

## Features

- Strict input validation (`<count>d<sides>[+|-modifier]`)
- Case-insensitive `d` (`2D6` works)
- No internal whitespace allowed
- Deterministic testing via injectable random provider
- CLI interface
- `--version` show version of diceroller
- `--verbose` human-readable output
- `--json` machine-readable output
- `--seed` optional seed for deterministic dice rolls
- Fully unit tested

---

## Installation

Clone the repo and install in editable mode:

```bash
pip install -e .
```

This installs the `diceroller` command into your virtual environment.

---

## CLI Usage

### Basic Roll

```bash
$ diceroller 2d6+1
7
```

### Verbose Output

```bash
$ diceroller 2d6+1 --verbose
7 ( 3 3 +1 )
```

### JSON Output

```bash
$ diceroller 2d6+1 --json
{
  "rolls": [
    6,
    3
  ],
  "modifier": 1,
  "total": 10,
  "dice_type": 6
}
```

### Seeded Rolls

```bash
$ diceroller 2d6+1 --seed 42
7
```

Adding `--seed` followed by an integer seeds the internal RNG so repeated rolls yield the same sequence.

---

## Supported Expression Format

```
<dice_count>[d|D]<dice_type>[+|-<modifier>]
```

### Rules

- `dice_count` must be ≥ 1  
- `dice_type` must be ≥ 1  
- `modifier` is optional and may be negative  
- No internal whitespace allowed  
- Leading/trailing whitespace is ignored  

### Valid Examples

| Expression | Meaning                      |
|------------|------------------------------|
| `1d6`      | Roll one six-sided die       |
| `2D8`      | Roll two eight-sided dice    |
| `3d4-1`    | Roll three d4 and subtract 1 |
| `10d20+5`  | Roll ten d20 and add 5       |

### Invalid Examples

- `d6`
- `2d`
- `0d6`
- `1d0`
- `1d6++2`
- `1d6 + 2`

---

## Running Tests

After installing editable:

```bash
pytest
```

The test suite covers:

- Expression validation
- Edge cases
- Modifier handling
- Multi-die rolls
- Deterministic random injection

---

## Architecture

Core logic is isolated from the CLI:

```
src/diceroller/
├── core.py   # Validation and rolling logic
└── cli.py    # Command-line interface
```

This separation keeps the dice engine reusable and independently testable.

---

## Programmatic Usage

```python
from diceroller.core import DiceRoller

roller = DiceRoller()
total = roller.roll("2d6+1")

print(roller.data.rolls)
print(roller.data.modifier)
print(total)
```
