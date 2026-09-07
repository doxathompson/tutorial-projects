import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from app import add_transaction,connect
class DatabaseTests(unittest.TestCase):
    def test_add_transaction(self):
        with tempfile.TemporaryDirectory() as raw:
            db=connect(Path(raw)/"test.db"); add_transaction(db,"Lunch",1250); self.assertEqual(db.execute("SELECT description,cents FROM transactions").fetchone(),("Lunch",1250))
    def test_rejects_invalid_transaction(self):
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaises(ValueError): add_transaction(connect(Path(raw)/"test.db"),"",0)
if __name__=="__main__": unittest.main()
