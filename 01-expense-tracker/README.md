# Expense Tracker

A dependency-free command-line expense tracker. It deliberately stores data in
JSON: the format is easy to inspect while learning and the repository boundary
makes a future switch to SQLite straightforward.

## Run

```bash
python expense_tracker.py --file expenses.json add 12.50 food "Lunch"
python expense_tracker.py --file expenses.json list
python expense_tracker.py --file expenses.json summary
python -m unittest discover -s tests -v
```

Money is represented as integer cents, never binary floating-point. Writes use
a temporary file followed by an atomic replace, preventing a crash halfway
through a write from corrupting the data file.

