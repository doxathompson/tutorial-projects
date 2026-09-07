import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from organizer import apply_moves, find_duplicates, plan_moves


class OrganizerTests(unittest.TestCase):
    def test_plan_does_not_change_files(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "photo.JPG"
            source.write_bytes(b"image")
            moves = plan_moves(root)
            self.assertTrue(source.exists())
            self.assertEqual(moves[0].destination, root / "images" / "photo.JPG")

    def test_apply_and_duplicate_detection(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "a.txt").write_text("same")
            (root / "b.txt").write_text("same")
            self.assertEqual(len(find_duplicates(root)), 1)
            apply_moves(plan_moves(root))
            self.assertTrue((root / "documents" / "a.txt").exists())


if __name__ == "__main__":
    unittest.main()
