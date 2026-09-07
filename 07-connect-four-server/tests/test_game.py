import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from server import Game
class GameTests(unittest.TestCase):
    def test_horizontal_win(self):
        game=Game()
        for column in (0,0,1,1,2,2): self.assertFalse(game.drop(column))
        self.assertTrue(game.drop(3))
    def test_invalid_column(self):
        with self.assertRaises(ValueError): Game().drop(7)
if __name__=="__main__":unittest.main()

