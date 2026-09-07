import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from expense_tracker import Expense, ExpenseRepository, add_expense, parse_money, summarize


class ExpenseTrackerTests(unittest.TestCase):
    def test_money_is_converted_exactly(self) -> None:
        self.assertEqual(parse_money("12.50"), 1250)
        with self.assertRaises(ValueError):
            parse_money("1.999")

    def test_ids_remain_monotonic_after_a_deletion(self) -> None:
        items = [Expense(2, 100, "food", "Tea", "2026-01-01")]
        self.assertEqual(add_expense(items, "2", "travel", "Bus").id, 3)

    def test_summary_groups_categories(self) -> None:
        items = [
            Expense(1, 150, "food", "Tea", "2026-01-01"),
            Expense(2, 250, "food", "Lunch", "2026-01-01"),
        ]
        self.assertEqual(summarize(items), {"food": 400})

    def test_repository_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = ExpenseRepository(Path(directory) / "expenses.json")
            expected = [Expense(1, 1250, "food", "Lunch", "2026-01-01")]
            repository.save(expected)
            self.assertEqual(repository.load(), expected)


if __name__ == "__main__":
    unittest.main()
