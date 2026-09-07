import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from tracker import connect,record
class TrackerTests(unittest.TestCase):
    def test_alerts_after_threshold(self):
        with tempfile.TemporaryDirectory() as raw:
            db=connect(Path(raw)/"p.db"); self.assertEqual(record(db,"u",100),(None,False)); self.assertEqual(record(db,"u",102),(100,True))
if __name__=="__main__": unittest.main()

