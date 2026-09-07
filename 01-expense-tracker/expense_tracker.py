"""A small CLI that demonstrates safe persistence and precise money handling."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Expense:
    id: int
    amount_cents: int
    category: str
    description: str
    spent_on: str


class ExpenseRepository:
    """Owns persistence so the rest of the application is storage-agnostic."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[Expense]:
        if not self.path.exists():
            return []
        try:
            rows = json.loads(self.path.read_text(encoding="utf-8"))
            return [Expense(**row) for row in rows]
        except (json.JSONDecodeError, TypeError, KeyError) as exc:
            raise ValueError(f"Cannot read expense data from {self.path}") from exc

    def save(self, expenses: Iterable[Expense]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps([asdict(item) for item in expenses], indent=2) + "\n"

        # Atomic replacement means readers see either the old complete file or
        # the new complete file, never a half-written document.
        descriptor, temp_name = tempfile.mkstemp(dir=self.path.parent, text=True)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as temp_file:
                temp_file.write(payload)
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.replace(temp_name, self.path)
        except BaseException:
            Path(temp_name).unlink(missing_ok=True)
            raise


def parse_money(raw: str) -> int:
    """Convert a decimal currency string to cents without float rounding bugs."""
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {raw}") from exc
    if value <= 0 or value.as_tuple().exponent < -2:
        raise ValueError("Amount must be positive with at most two decimal places")
    return int(value * 100)


def add_expense(
    existing: list[Expense], amount: str, category: str, description: str
) -> Expense:
    next_id = max((item.id for item in existing), default=0) + 1
    expense = Expense(
        id=next_id,
        amount_cents=parse_money(amount),
        category=category.strip().lower(),
        description=description.strip(),
        spent_on=date.today().isoformat(),
    )
    if not expense.category or not expense.description:
        raise ValueError("Category and description cannot be empty")
    existing.append(expense)
    return expense


def summarize(expenses: Iterable[Expense]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for item in expenses:
        totals[item.category] += item.amount_cents
    return dict(sorted(totals.items()))


def format_money(cents: int) -> str:
    return f"${cents / 100:.2f}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track personal expenses")
    parser.add_argument("--file", type=Path, default=Path("expenses.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="record an expense")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("description")
    commands.add_parser("list", help="show all expenses")
    commands.add_parser("summary", help="total expenses by category")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repository = ExpenseRepository(args.file)
    try:
        expenses = repository.load()
        if args.command == "add":
            item = add_expense(expenses, args.amount, args.category, args.description)
            repository.save(expenses)
            print(f"Added #{item.id}: {format_money(item.amount_cents)}")
        elif args.command == "list":
            for item in expenses:
                print(f"#{item.id} {item.spent_on} {item.category:<12} "
                      f"{format_money(item.amount_cents):>10}  {item.description}")
        else:
            for category, cents in summarize(expenses).items():
                print(f"{category:<12} {format_money(cents):>10}")
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

